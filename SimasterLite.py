import mysql.connector
import pandas as pd
import numpy as np
import smtplib 
from datetime import datetime
from validate_email import validate_email

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="a1234567akristal",
    database = 'sister'
)

mycursor = mydb.cursor()

def signup() :
    print('SIGN UP PAGE' + '\n' + '\n')
    signup = True
    while(signup == True) :

        nama = input('Nama : ')

        boolean = True
        while(boolean == True) :
            try :
                nim = input('NIM Lengkap : ')
                nim = nim.split('/')
                niu = nim[1]
                angkatan = '20{tahun}'.format(tahun = nim[0])
                nim = nim[3]
                boolean = False
            except :
                print('NIM Lengkap Invalid!')
                boolean = True
    
        boolean = True
        while(boolean == True) :
            prodi = input('Pilih Jurusanmu : ' + '\n' + '\n' +
                            '1. Teknologi Informasi' + '\n' +
                            '2. Teknik Elektro' + '\n' +
                            '3. Teknik Biomedis' + '\n' +
                            'Jurusan : ')
            if prodi not in ['1','2','3'] :
                print('\n' + 'Pilihan Invalid!')
                boolean = True
            else :
                if prodi == '1' :
                    prodi = 'Teknologi Informasi'
                elif prodi == '2' :
                    prodi = 'Teknik Elektro'
                elif prodi == '3' :
                    prodi = 'Teknik Biomedis'
                boolean = False

        boolean = True
        while(boolean == True) :
            email = input('Email UGM : ')
            check_email = email.split('@')
            check_email = check_email[1]
            is_valid = validate_email(email,verify=True)
            if check_email == 'mail.ugm.ac.id' :
                if is_valid == True :
                    boolean = False
                else :
                    boolean = True
                    print('Email UGM belum ter-verifikasi!')
            else :
                print('Masukkan email UGM!')
                boolean = True
            
        check = signup_check(niu, nim, email)
        if check == 1 :
            signup = False
            sql = "INSERT INTO sister.student (nama_siswa, nim, niu, jurusan, angkatan, email) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (nama, nim, niu, prodi, int(angkatan), email)
            mycursor.execute(sql, val)

            mydb.commit()
            print('Sign Up berhasil!')
            signin()
        elif check == 2 :
            print('Email / NIM sudah terdaftar!')
            signin_req = input('Sudah punya akun? (Y/N) : ')
            if signin_req == 'Y' or signin_req == 'y' :
                signup = False
                signin()
            else :
                signup = True

def signup_check(niu, nim, email) :
    sql = "select * from student where student.niu = %s or student.nim = %s or student.email = %s"
    val = (niu, nim, email,)
    mycursor.execute(sql, val)
    check = mycursor.fetchall()

    if len(check) == 0 :
        return 1
    else :
        return 2

def signin() :
    print('SIGN IN PAGE' + '\n')
    signin = True
    while(signin == True) :
        niu = input('NIU : ')
        email = input('Email UGM : ' + '\n')
    
        sql = "select * from student where student.niu = %s"
        val = (niu,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        df = pd.DataFrame(myresult)
        
        if len(df) == 0 :
            print('')
            print('Data mahasiswa tidak ditemukan!')
            signup_req = input('Belum punya akun? (Y/N) : ')
            if signup_req == 'Y' or signup_req == 'y' :
                signin = False
                signup()
            else :
                signin = True
        else :
            if email != df[6][0] :
                print('')
                print('Email salah!')
                signin = True
            else :
                signin = False
                print('')
                print('Sign In Berhasil!')
                student_menu(df)

def main(role) :
    print('SELAMAT DATANG DI SIMASTER LITE!' + '\n')
    boolean = True
    while (boolean == True) :
        menu = input('MENU'+ '\n' + '1. Sign In' + '\n' +
                    '2. Sign Up' + '\n\n')
        print('')
        if menu in ['1', '2'] :
            boolean = False
            if role == '1' :
                if menu == '1' :
                    signin()
                else :
                    signup()
            else :
                if menu == '1' :
                    dosen_signin()
                else :
                    signup_dosen()
        else :
            print('')
            print('Input tidak dikenali!')
            input('')

def student_menu(df) :
    df = df
    nama = df[1][0]
    niu = df[3][0]
    nim = df[2][0]
    prodi = df[4][0]
    angkatan = df[5][0]
    email = df[6][0]
    student_id = df[0][0]
    
    print('')
    print('PROFIL MAHASISWA')
    print('Nama : {namaa}'.format(namaa = nama))
    print('NIU : {niuu}'.format(niuu = niu))
    print('NIF : {nimm}'.format(nimm = nim))
    print('Jurusan : {jur}'.format(jur = prodi))
    print('Angkatan : {angk}'.format(angk = angkatan))
    print('Email : {emaill}'.format(emaill = email))
    
    print('')
    print('MENU MAHASISWA')
    boolean = True
    while(boolean == True) :
        menu = input('1. Lihat Mata Kuliah tersedia' + '\n' +
                '2. Lihat Mata Kuliah yang diikuti' + '\n'
                '3. Lihat Tugas' + '\n')
        if menu == '1' :
            boolean = False
            matkul(student_id, df)
        elif menu == '2' :
            boolean = False
            subscription(student_id, df)
        elif menu == '3' :
            boolean = False
            tugas(student_id, df)
        else :
            print('')
            print('Input tidak dikenali!')
            input('')

def matkul(student_id, df_fix) :
    print('')
    print('MATA KULIAH')
    matkul = True
    while (matkul == True) :
        menu = input('1. Search Mata Kuliah' + '\n' +
                    '2. Tampilkan seluruh Mata Kuliah' + '\n' +
                    '3. Subscribe ke Mata Kuliah' + '\n' +
                    '4. Kembali ke Menu Mahasiswa' + '\n')
    
        if menu == '2' :
            sql = "select matkul.matkul_id, matkul.nama_matkul, matkul.hari, matkul.jam_mulai, matkul.jam_selesai from sister.matkul"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            df = pd.DataFrame(myresult)
            df[3] = df[3].astype(str)
            df[4] = df[4].astype(str)
            df[3] = df[3].apply(get_time)
            df[4] = df[4].apply(get_time)
            print('Jadwal Mata Kuliah')
            for i in range(0, len(df)) :
                print('Nama Matkul : {nama}'.format(nama = df[1][i]))
                print('Hari : {hari}'.format(hari = df[2][i]))
                print('Jam : {mulai} - {selesai}'.format(mulai = df[3][i], selesai = df[4][i]))
                print('Kode Kelas : {class_id}'.format(class_id = df[0][i]))
                print('')
        
        elif menu == '1':
            boolean = True
            while(boolean == True) :
                search = input('Search Nama Matkul : ')
                sql = "select matkul.matkul_id, matkul.nama_matkul, matkul.hari, matkul.jam_mulai, matkul.jam_selesai from matkul where lower(nama_matkul) like '%{nama}%' or nama_matkul like '%{nama}%' or upper(nama_matkul) like '%{nama}%'".format(nama = search)
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                df = pd.DataFrame(myresult)
                df[3] = df[3].astype(str)
                df[4] = df[4].astype(str)
                df[3] = df[3].apply(get_time)
                df[4] = df[4].apply(get_time)
                if len(df) == 0 :
                    print('Data Kelas tidak ditemukan!')
                else :
                    boolean = False
                    print('')
                    print('Jadwal Mata Kuliah')
                    for i in range(0, len(df)) :
                        print('Nama Matkul : {nama}'.format(nama = df[1][i]))
                        print('Hari : {hari}'.format(hari = df[2][i]))
                        print('Jam : {mulai} - {selesai}'.format(mulai = df[3][i], selesai = df[4][i]))
                        print('Kode Kelas : {class_id}'.format(class_id = df[0][i]))
                        print('')
        
        elif menu == '3' :
            subs = True
            while(subs == True) :
                sub_class = int(input('Masukkan Kode Kelas yang ingin diikuti : '))
                sql = "select matkul.matkul_id from matkul where matkul_id = {code}".format(code = sub_class)
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
            
                if len(myresult) == 0 :
                    print('Kelas Tidak Ditemukan!')
                else :
                    subs = False
                    sql = "select * from sister.subscription where student_id = {studid} and matkul_id = {matid}".format(studid = int(student_id), matid = int(sub_class))
                    mycursor.execute(sql)
                    myresult2 = mycursor.fetchall()
                    if len(myresult2) == 0 :
                        sql = "INSERT INTO sister.subscription (student_id, matkul_id, sub_time) VALUES (%s, %s, %s)"
                        val = (int(student_id), int(sub_class), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        mycursor.execute(sql, val)

                        mydb.commit()
                        print('')
                        print('Subscription Berhasil!')
                    else :
                        print('')
                        print('Kelas sudah diikuti!')
                        input()
                    
        elif menu == '4' :
            matkul = False
            student_menu(df_fix)
        else :
            print('')
            print('Input tidak dikenali!')
            input('')

def subscription(student_id, df_fix) :
    sql = '''select matkul.matkul_id, matkul.nama_matkul, matkul.hari, matkul.jam_mulai, matkul.jam_selesai
            from sister.matkul
            inner join sister.subscription
            on matkul.matkul_id = subscription.matkul_id
            where subscription.student_id = {studid}'''.format(studid = student_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if len(myresult) == 0 :
        print('')
        print('Belum ada kelas yang diikuti!')
        input('')
        student_menu(df_fix)
    else :
        subs = True
        while (subs == True) :
            sql = '''select matkul.matkul_id, matkul.nama_matkul, matkul.hari, matkul.jam_mulai, matkul.jam_selesai
            from sister.matkul
            inner join sister.subscription
            on matkul.matkul_id = subscription.matkul_id
            where subscription.student_id = {studid}'''.format(studid = student_id)
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            df = pd.DataFrame(myresult)
            df[3] = df[3].astype(str)
            df[4] = df[4].astype(str)
            df[3] = df[3].apply(get_time)
            df[4] = df[4].apply(get_time)
            kelas_sub = df[0].tolist()
            
            print('')
            print('KELAS YANG DIIKUTI')
            for i in range(0, len(df)) :
                print('Nama Matkul : {nama}'.format(nama = df[1][i]))
                print('Hari : {hari}'.format(hari = df[2][i]))
                print('Jam : {mulai} - {selesai}'.format(mulai = df[3][i], selesai = df[4][i]))
                print('Kode Kelas : {class_id}'.format(class_id = df[0][i]))
                print('')
        
            print('SUBSCRIPTION MENU')
            menu = input('1. Unsubscribe dari sebuah kelas' + '\n' +
                        '2. Lihat tugas kelas' + '\n' +
                        '3. Kembali ke Menu Mahasiswa' + '\n')
    
            if menu == '1' :
                unsub = True
                while(unsub == True) :
                    matkulid = int(input('Masukkan Kode Kelas yang ingin ditinggalkan : '))
                    if matkulid in kelas_sub :
                        unsub = False
                        sql = "DELETE FROM subscription WHERE student_id = student_id and matkul_id = {kode}".format(kode = matkulid)
                        mycursor.execute(sql)
                        mydb.commit()
                        print('')
                        print('Kelas berhasil ditinggalkan!')
                    else :
                        print('')
                        print('Kelas tidak terdaftar sebagai kelas yang diikuti!')
        
            elif menu == '2' :
                tugas = True
                while (tugas == True) :
                    matkulid = int(input('Masukkan Kode Kelas yang ingin dilihat' + '\n'))
                    if matkulid in kelas_sub :
                        tugas = False
                        sql = 'SELECT matkul.nama_matkul, matkul_items.* FROM sister.matkul_items inner join sister.matkul on matkul_items.matkul_id = matkul.matkul_id where matkul.matkul_id = {matkull}'.format(matkull = matkulid)
                        mycursor.execute(sql)
                        myresult2 = mycursor.fetchall()
                        if len(myresult2) == 0 :
                            print('Tidak ada tugas!')
                            input('')
                        else :
                            df2 = pd.DataFrame(myresult2)
                            df2 = df2.sort_values(by = 3, ascending = False)
                            df2.reset_index(inplace = True, drop = True)
                            print('')
                            print('TUGAS MATA KULIAH {nama_mat}'.format(nama_mat = df2[0][0]))
                            for i in range(0, len(df2)) :
                                print('Tipe : ' + str(df2[2][i]))
                                print('Keterangan : ' + str(df2[4][i]))
                                print('Deadline : ' + str(df2[3][i]))
                                print('')
                            input('')
                    else :
                        print('')
                        print('Kelas tidak terdaftar sebagai kelas yang diikuti!')
                    
            elif menu == '3' :
                subs = False
                student_menu(df_fix)
            else :
                print('')
                print('Input tidak dikenali!')
                input('')

def tugas(student_id, df_fix) :
    sql = '''select raw1.* from
            (select matkul.matkul_id, matkul.nama_matkul, matkul_items.tipe, matkul_items.keterangan, matkul_items.deadline
            from sister.matkul_items
            inner join sister.matkul
            on matkul.matkul_id = matkul_items.matkul_id) as raw1
            inner join sister.subscription
            on raw1.matkul_id = subscription.matkul_id
            where subscription.student_id = {studid}'''.format(studid = int(student_id))
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if len(myresult) == 0 :
        print('')
        print('Tidak ada tugas!')
    else :
        df = pd.DataFrame(myresult)
        print('')
        print('LIST TUGAS')
        df = df.sort_values(by = 4, ascending = True)
        df.reset_index(inplace = True, drop = True)
        for i in range(0, len(df)) :
            print('Mata Kuliah : ' + str(df[1][i]))
            print('Tipe : ' + str(df[2][i]))
            print('Keterangan : ' + str(df[3][i]))
            print('Deadline : ' + str(df[4][i]))
            print('')
    kembali = input('Kembali ke Menu Mahasiswa? (Y/N)')
    if kembali == 'Y' or kembali == 'y' :
        student_menu(df_fix)
    else :
        input()
        student_menu(df_fix)

def get_time(time) :
    time = time.split('days ')
    time = time[1]
    return time

def start() :
    boolean = True
    while(boolean == True) :
        role = input('1. As Student' + '\n' +
                    '2. As Admin' + '\n')
        if role in ['1', '2'] :
            boolean = False
            main(role)
        else :
            print('')
            print('Input tidak dikenali!')

def dosen_signin() :
    print('SIGN IN PAGE' + '\n')
    signin = True
    while(signin == True) :
        nidn = input('NIDN : ')
        email = input('Email UGM : ' + '\n')
    
        sql = "select * from dosen where dosen.nidn = %s"
        val = (nidn,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        df = pd.DataFrame(myresult)
        
        if len(df) == 0 :
            print('')
            print('Data Admin tidak ditemukan!')
            signup_req = input('Belum punya akun? (Y/N) : ')
            if signup_req == 'Y' or signup_req == 'y' :
                signin = False
                signup_dosen()
            else :
                signin = True
        else :
            if email != df[2][0] :
                print('')
                print('Email salah!')
                signin = True
            else :
                signin = False
                print('')
                print('Sign In Berhasil!')
                dosen_menu(df)

def signup_dosen() :
    print('SIGN UP PAGE' + '\n' + '\n')
    signup = True
    while(signup == True) :

        nama = input('Nama : ')
        nidn = input('NIDN : ')
        nomor = input('No. Handphone : ')
        
        boolean = True
        while(boolean == True) :
            email = input('Email UGM : ')
            check_email = email.split('@')
            check_email = check_email[1]
            is_valid = validate_email(email,verify=True)
            if check_email == 'ugm.ac.id' :
                if is_valid == True :
                    boolean = False
                else :
                    boolean = True
                    print('Email UGM belum ter-verifikasi!')
            else :
                print('Masukkan email UGM!')
                boolean = True
            
        check = signup_check_dosen(nidn, email)
        if check == 1 :
            signup = False
            sql = "INSERT INTO sister.dosen (nama_dosen, email, nomor, nidn, email_fake) VALUES (%s, %s, %s, %s, %s)"
            val = (nama, email, nomor, nidn, 'sylvesterleond@gmail.com')
            mycursor.execute(sql, val)

            mydb.commit()
            print('Sign Up berhasil!')
            dosen_signin()
        elif check == 2 :
            print('Email / NIM sudah terdaftar!')
            signin_req = input('Sudah punya akun? (Y/N) : ')
            if signin_req == 'Y' or signin_req == 'y' :
                signup = False
                dosen_signin()
            else :
                signup = True
                
def signup_check_dosen(nidn, email) :
    sql = "select * from dosen where dosen.nidn = %s or dosen.email = %s"
    val = (nidn, email,)
    mycursor.execute(sql, val)
    check = mycursor.fetchall()

    if len(check) == 0 :
        return 1
    else :
        return 2

def dosen_menu(df) :
    df = df
    nama = df[1][0]
    email = df[2][0]
    nomor = df[3][0]
    nidn = df[4][0]
    dosen_id = df[0][0]
    
    print('')
    print('PROFIL ADMIN')
    print('Nama : {namaa}'.format(namaa = nama))
    print('NIDN : {nidnn}'.format(nidnn = nidn))
    print('Email : {emaill}'.format(emaill = email))
    print('No. Handphone : {no}'.format(no = nomor))
    
    print('')
    print('MENU ADMIN')
    boolean = True
    while(boolean == True) :
        menu = input('1. Lihat Mata Kuliah Diampu' + '\n' +
                '2. Tambah Mata Kuliah Diampu' + '\n'
                '3. Lihat Tugas' + '\n'
                    )
        if menu == '1' :
            boolean = False
            matkul_dosen(dosen_id, df)
        elif menu == '2' :
            boolean = False
            tambah_matkul(dosen_id, df)
        elif menu == '3' :
            boolean = False
            tugas_dosen(dosen_id, df)
        else :
            print('')
            print('Input tidak dikenali!')
            input('')
        
def matkul_dosen(dosen_id, df_fix) :
    print('DAFTAR MATKUL DIAMPU')
    sql = "select * from matkul where matkul.dosen_id = %s"
    val = (int(dosen_id),)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    if(len(myresult) == 0) :
        print('')
        print('Belum ada Mata Kuliah yang di ampu!')
        input()
        dosen_menu(df_fix)
    else :
        df = pd.DataFrame(myresult)
        df[4] = df[4].astype(str)
        df[5] = df[5].astype(str)
        df[4] = df[4].apply(get_time)
        df[5] = df[5].apply(get_time)
        class_code = df[0].tolist()
        
        print('Jadwal Mata Kuliah')
        for i in range(0, len(df)) :
            print('Nama Matkul : {nama}'.format(nama = df[1][i]))
            print('Hari : {hari}'.format(hari = df[2][i]))
            print('Jam : {mulai} - {selesai}'.format(mulai = df[3][i], selesai = df[4][i]))
            print('Kode Kelas : {class_id}'.format(class_id = df[0][i]))
            print('')
        
        boolean = True
        while boolean == True :
            action = input('1. Tambah Mata Kuliah' + '\n' + '2. Tambah Tugas' + '\n' + '3. Kembali ke Menu Dosen' + '\n')
            if action == '1' :
                boolean = False
                tambah_matkul(dosen_id, df_fix)
            elif action == '3' :
                boolean = False
                dosen_menu(df_fix)
            elif action == '2' :
                boolean = False
                action = True
                while action == True :
                    kode = input('Masukkan Kode Kelas : ')
                    if int(kode) in class_code :
                        action = False
                        tambah_tugas(int(kode), df_fix)
                    else :
                        print('')
                        print('Kode Kelas invalid!')
                
            else :
                print('')
                print('Input tidak dikenali!')

def tambah_matkul(dosen_id, df_fix) :
    print('TAMBAH MATKUL')
    tambah = True
    while(tambah == True) :
        nama = input('Nama Matkul : ')
        boolean = True
        while(boolean == True) :
            hari = input('Hari : ' + '\n' +
                        '1. Senin' + '\n' +
                        '2. Selasa' + '\n' +
                        '3. Rabu' + '\n' +
                        '4. Kamis' + '\n' +
                        '5. Jumat' + '\n')
            if hari in ['1', '2', '3', '4', '5'] :
                boolean = False
                if hari == '1' :
                    hari = 'Senin'
                elif hari == '2' :
                    hari = 'Selasa'
                elif hari == '3' :
                    hari = 'Rabu'
                elif hari == '4' :
                    hari = 'Kamis'
                else :
                    hari = 'Jumat'
        
        jam_mulai = input('Jam Mulai (HH:mm:ss) : ')
        jam_selesai = input('Jam Selesai (HH:mm:ss) : ')
        
        sql = "INSERT INTO sister.matkul (nama_matkul, dosen_id, hari, jam_mulai, jam_selesai) VALUES (%s, %s, %s, %s, %s)"
        val = (nama, int(dosen_id), hari, jam_mulai, jam_selesai)
        mycursor.execute(sql, val)

        mydb.commit()
        print('Mata Kuliah berhasil ditambahkan!')
        kembali = input('Selesai menambahkan Mata Kuliah? (Y/N)')
        
        if kembali == 'Y' or kembali == 'y' :
            tambah = False
            dosen_menu(df_fix)

def tugas_dosen(dosen_id, df_fix) :
    print('')
    print('DAFTAR TUGAS')
    sql = '''select matkul.nama_matkul, matkul_items.tipe, matkul_items.keterangan, matkul_items.deadline
            from matkul_items inner join matkul on matkul_items.matkul_id = matkul.matkul_id
            where matkul.dosen_id = {dosid}'''.format(dosid = dosen_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if len(myresult) == 0 :
        print('')
        print('Tidak ada tugas!')
    else :
        df = pd.DataFrame(myresult)
        df = df.sort_values(by = 3, ascending = True)
        df.reset_index(inplace = True, drop = True)
        for i in range(0, len(df)) :
            for i in range(0, len(df)) :
                print('Mata Kuliah : ' + str(df[0][i]))
                print('Tipe : ' + str(df[1][i]))
                print('Keterangan : ' + str(df[2][i]))
                print('Deadline : ' + str(df[3][i]))
                print('')
                
    boolean = True
    while boolean == True :
        action = input('1. Tambah tugas' + '\n' + '2. Kembali ke menu dosen' + '\n')
        if action == '1' :
            boolean = False
            matkul_dosen(dosen_id, df_fix)
        elif action == '2' :
            boolean = False
            dosen_menu(df_fix)
        else :
            print('')
            print('Input tidak dikenali!')

def tambah_tugas(matkul_id, df_fix) :
    print('TAMBAH TUGAS')
    tambah = True
    while tambah == True :
        boolean = True
        while boolean == True :
            tipe = input('1. Tugas' + '\n' + '2. Quiz' + '\n')
            if tipe in ['1', '2'] :
                boolean = False
                if tipe == '1' :
                    tipe = 'Tugas'
                else :
                    tipe = 'Quiz'
            else :
                print('Input tidak dikenali!')
        
        deadline = input('Deadline tugas (YYYY-MM-DD HH:mm:ss) : ')
        keterangan = input('Keterangan : ')
        
        sql = "INSERT INTO sister.matkul_items (tipe, deadline, keterangan, matkul_id) VALUES (%s, %s, %s, %s)"
        val = (tipe, deadline, keterangan, int(matkul_id))
        mycursor.execute(sql, val)

        mydb.commit()
        print('Tugas berhasil ditambahkan!')
        
        send(matkul_id, tipe, deadline, keterangan)
        print('Notifikasi berhasil dikirimkan!')
        
        kembali = input('Kembali ke Menu Dosen? (Y/N)')
        if kembali == 'Y' or kembali == 'y' :
            tambah = False
            dosen_menu(df_fix)
        else :
            input('')
            dosen_menu(df_fix)

def send(matkul_id, tipe, deadline, keterangan) :
    sql = '''select subscription.matkul_id, student.student_id, student.email, matkul.nama_matkul
            from subscription inner join student on subscription.student_id = student.student_id
            inner join matkul on subscription.matkul_id = matkul.matkul_id
            where subscription.matkul_id = {matid}'''.format(matid = matkul_id)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if len(myresult) == 0 :
        return 'Notifikasi tidak dikirimkan ke siapapun!'
    else :
        try : 
            df = pd.DataFrame(myresult)
            nama_matkul = df[3][0]
            for i in range(0, len(df)) : 
                s = smtplib.SMTP('smtp.gmail.com', 587) 
                s.starttls() 
                s.login("sylvesterleond@gmail.com", "a1234567akristal") 
                message = '''Info Kelas {nama}
Tipe : {tipee}
Keterangan : {ket}
Deadline : {dead}'''.format(nama = nama_matkul, tipee = tipe, ket = keterangan, dead = deadline)
                #print(message)
                s.sendmail("sylvesterleond@gmail.com", df[2][i], message) 
                s.quit() 
            return 'Notifikasi berhasil dikirimkan!'
        except :
            return 'Failed'

start()
