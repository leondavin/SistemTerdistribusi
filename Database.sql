CREATE TABLE student (
student_id int NOT NULL auto_increment,
nama_siswa varchar(100) NOT NULL,
nim varchar(5) NOT NULL,
niu varchar(6) NOT NULL,
jurusan varchar(20) NOT NULL,
angkatan int NOT NULL,
email varchar(50) NOT NULL,
PRIMARY KEY (student_id)
);

CREATE TABLE dosen (
dosen_id int NOT NULL auto_increment,
nama_dosen varchar(100) NOT NULL,
email varchar(50) NOT NULL,
nomor varchar(15) NOT NULL,
nidn varchar(20) NOT NULL,
email_fake varchar(50) NOT NULL,
PRIMARY KEY (dosen_id)
);

CREATE TABLE matkul(
matkul_id int NOT NULL auto_increment,
nama_matkul varchar(50) NOT NULL,
dosen_id int NOT NULL,
hari varchar(6) NOT NULL,
jam_mulai time NOT NULL,
jam_selesai time NOT NULL,
PRIMARY KEY (matkul_id),
FOREIGN KEY (dosen_id) REFERENCES dosen(dosen_id)
);

CREATE TABLE subscription (
subscription_id int NOT NULL auto_increment,
student_id int NOT NULL,
matkul_id int NOT NULL,
sub_time datetime NOT NULL,
PRIMARY KEY (subscription_id),
FOREIGN KEY (student_id) REFERENCES student(student_id),
FOREIGN KEY (matkul_id) REFERENCES matkul(matkul_id)
);

CREATE TABLE matkul_items (
item_id int NOT NULL auto_increment,
tipe varchar(20) NOT NULL,
deadline datetime NOT NULL,
keterangan varchar(200) NOT NULL,
matkul_id int NOT NULL,
PRIMARY KEY (item_id),
FOREIGN KEY (matkul_id) REFERENCES matkul(matkul_id)
);

insert into sister.student (nama_siswa, nim, niu, jurusan, angkatan, email)
values ('Leon Davin', '47574', '429072', 'Teknologi Informasi', '2018', 'leondavin@mail.ugm.ac.id'),
('Kristianto Haryodi', '47008', '425313', 'Teknologi Informasi', '2018', 'kristiantoharyodi@mail.ugm.ac.id'),
('Chlenysis Kamela Manurung', '47982', '431389', 'Teknologi Informasi', '2018', 'chlenysiskamela@mail.ugm.ac.id'),
('Bagas Muhammad A.D.', '47981', '431388', 'Teknologi Informasi', '2018', 'bagas.m@mail.ugm.ac.id'),
('Christianto Natalio Saleky', '48015', '431998', 'Teknologi Informasi', '2018', 'christianto.natalio.saleky@mail.ugm.ac.id');

insert into sister.dosen(nama_dosen, email, nomor, nidn, email_fake)
values ('Ir. Lukito Edi Nugroho, M.Sc., Ph.D.', 'lukito@ugm.ac.id', '123123123', '123', 'sylvesterleond@gmail.com'),
('Dr. Ir. Rudy Hartanto, M.T.', 'rudy@ugm.ac.id', '123123123', '124', 'sylvesterleond@gmail.com'),
('Dr. Ir. Risanuri Hidayat, M.Sc.', 'risanuri@ugm.ac.id', '123123123', '125', 'sylvesterleond@gmail.com');

insert into sister.matkul(nama_matkul, dosen_id, hari, jam_mulai, jam_selesai)
values ('Interoperabilitas', 1, 'Senin', '10:00', '12:00'),
('Sistem Terdistribusi', 1, 'Kamis', '10:00', '12:00'),
('Teknologi Multimedia', 2, 'Senin', '13:00', '15:00'),
('Arsitektur Komputer', 3, 'Jumat', '13:00', '15:00');

insert into sister.matkul_items(tipe, deadline, keterangan, matkul_id)
values ('Tugas', '2020-12-01 23:59:59', 'Pengumpulan video dan PPT aplikasi Interoperabilitas', 1),
('Tugas', '2020-12-04 23:59:59', 'Pengumpulan video dan PPT aplikasi Sistem Terdistribusi', 2),
('Tugas', '2020-11-30 13:00:00', 'Pengumpulan video dan PPT', 3);

insert into sister.subscription(student_id, matkul_id, sub_time)
values(1, 1, '2020-10-15 15:00:00'),
(1, 2, '2020-10-15 15:00:00'),
(1, 3, '2020-10-15 15:00:00'),
(1, 4, '2020-10-15 15:00:00'),
(2, 1, '2020-10-15 15:00:00'),
(2, 2, '2020-10-15 15:00:00'),
(2, 3, '2020-10-15 15:00:00'),
(3, 1, '2020-10-15 15:00:00'),
(3, 3, '2020-10-15 15:00:00'),
(3, 4, '2020-10-15 15:00:00'),
(4, 1, '2020-10-15 15:00:00'),
(4, 2, '2020-10-15 15:00:00'),
(5, 2, '2020-10-15 15:00:00'),
(5, 3, '2020-10-15 15:00:00');