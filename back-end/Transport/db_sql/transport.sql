-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Czas generowania: 07 Lut 2021, 16:31
-- Wersja serwera: 10.4.17-MariaDB
-- Wersja PHP: 8.0.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `transportmicroservice`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `couriers`
--

CREATE TABLE `couriers` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Zrzut danych tabeli `couriers`
--

INSERT INTO `couriers` (`id`, `name`) VALUES
(1, 'WorldWide Optics Corporation'),
(2, 'Advanced Research Corp.'),
(3, 'National Space Explore Co.'),
(4, 'Smart Mining Corporation'),
(5, 'Global High-Technologies Corp.'),
(6, 'First 2G Wireless Corporation'),
(7, 'Future Industry Corporation'),
(8, 'West I-Mobile Group'),
(9, 'United Logics Group'),
(10, 'Home Space Research Inc.');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `packages`
--

CREATE TABLE `packages` (
  `id` int(11) NOT NULL,
  `id_library_sender` varchar(255) DEFAULT NULL,
  `id_library_receiver` varchar(255) DEFAULT NULL,
  `id_book` varchar(255) DEFAULT NULL,
  `id_courier` int(11) DEFAULT NULL,
  `package_number` varchar(255) DEFAULT NULL,
  `delivery_stage` enum('PRZYGOTOWANIE_DO_NADANIA','ODEBRANA_PRZEZ_KURIERA','W_TRASNPORCIE','ODEBRANA_OD_KURIERA','GOTOWA_DO_ODBIORU') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Zrzut danych tabeli `packages`
--

INSERT INTO `packages` (`id`, `id_library_sender`, `id_library_receiver`, `id_book`, `id_courier`, `package_number`, `delivery_stage`) VALUES
(1, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '568', 2, 'DT-686493862-IL', 'GOTOWA_DO_ODBIORU'),
(2, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '570', 3, 'CB-232050715-ES', 'ODEBRANA_OD_KURIERA'),
(3, '5fd66f6263bde330b052cb2d', '5fd66f6263bde330b052cb2f', '827', 1, 'CM-904221761-BR', 'ODEBRANA_PRZEZ_KURIERA'),
(4, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '271', 1, 'CQ-987895463-US', 'GOTOWA_DO_ODBIORU'),
(5, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '802', 2, 'PV-143365730-SE', 'ODEBRANA_PRZEZ_KURIERA'),
(6, '5fd66f6263bde330b052cb2d', '5fd66f6263bde330b052cb2f', '467', 9, 'PQ-629469370-US', 'W_TRASNPORCIE'),
(7, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '903', 8, 'DP-815536812-IT', 'GOTOWA_DO_ODBIORU'),
(8, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '019', 10, 'AT-407102402-IL', 'ODEBRANA_OD_KURIERA'),
(9, '5fd66f6263bde330b052cb2d', '5fd66f6263bde330b052cb2f', '996', 3, 'ZM-232050729-SE', 'W_TRASNPORCIE'),
(10, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '161', 2, 'LM-143365743-GB', 'PRZYGOTOWANIE_DO_NADANIA'),
(11, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '436', 8, 'NN-904221775-CA', 'GOTOWA_DO_ODBIORU'),
(12, '5fd66f6263bde330b052cb2d', '5fd66f6263bde330b052cb2f', '750', 1, 'VV-775178859-IT', 'PRZYGOTOWANIE_DO_NADANIA'),
(13, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '513', 4, 'DT-540784398-DK', 'PRZYGOTOWANIE_DO_NADANIA'),
(14, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '439', 6, 'NU-232050732-US', 'ODEBRANA_OD_KURIERA'),
(15, '5fd66f6263bde330b052cb2d', '5fd66f6263bde330b052cb2f', '121', 1, 'CT-143365757-DK', 'W_TRASNPORCIE'),
(16, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '694', 7, 'NJ-686493876-BE', 'W_TRASNPORCIE'),
(17, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '935', 10, 'ZB-318417427-AU', 'GOTOWA_DO_ODBIORU'),
(18, '5fd66f6263bde330b052cb2d', '5fd66f6263bde330b052cb2f', '234', 2, 'DH-775178862-AT', 'W_TRASNPORCIE'),
(19, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '935', 8, 'NY-629469383-US', 'GOTOWA_DO_ODBIORU'),
(20, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '930', 1, 'CG-540784407-DE', 'ODEBRANA_PRZEZ_KURIERA'),
(21, '5fd66f6263bde330b052cb2d', '5fd66f6263bde330b052cb2f', '433', 4, 'PC-686493880-GB', 'ODEBRANA_PRZEZ_KURIERA'),
(22, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '253', 4, 'PK-407102416-US', 'W_TRASNPORCIE'),
(23, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '506', 6, 'EY-815536826-BR', 'W_TRASNPORCIE'),
(24, '5fd66f6263bde330b052cb2d', '5fd66f6263bde330b052cb2f', '622', 8, 'CA-629469397-DK', 'GOTOWA_DO_ODBIORU'),
(25, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '845', 6, 'VH-540784415-ES', 'GOTOWA_DO_ODBIORU'),
(26, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '678', 8, 'BW-629469406-IL', 'GOTOWA_DO_ODBIORU'),
(27, '5fd66f6263bde330b052cb2d', '5fd66f6263bde330b052cb2f', '081', 1, 'VZ-540784424-BR', 'ODEBRANA_OD_KURIERA'),
(28, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '405', 2, 'PQ-904221789-SE', 'GOTOWA_DO_ODBIORU'),
(29, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '648', 10, 'PC-629469410-DK', 'ODEBRANA_PRZEZ_KURIERA'),
(30, '5fd66f6263bde330b052cb2d', '5fd66f6263bde330b052cb2f', '859', 8, 'AP-540784438-SE', 'GOTOWA_DO_ODBIORU'),
(31, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '327', 3, 'VM-815536830-AU', 'GOTOWA_DO_ODBIORU'),
(32, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '864', 4, 'VT-775178876-GR', 'GOTOWA_DO_ODBIORU'),
(33, '5fd66f6263bde330b052cb2d', '5fd66f6263bde330b052cb2f', '738', 8, 'PI-318417435-DE', 'ODEBRANA_PRZEZ_KURIERA'),
(34, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '300', 2, 'LX-904221792-US', 'PRZYGOTOWANIE_DO_NADANIA'),
(35, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '071', 9, 'ZF-407102420-SE', 'W_TRASNPORCIE'),
(36, '5fd66f6263bde330b052cb2d', '5fd66f6263bde330b052cb2f', '801', 5, 'ZW-318417444-IT', 'GOTOWA_DO_ODBIORU'),
(37, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '792', 4, 'DF-629469423-GR', 'GOTOWA_DO_ODBIORU'),
(38, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '786', 2, 'CP-232050746-DK', 'GOTOWA_DO_ODBIORU'),
(39, '5fd66f6263bde330b052cb2d', '5fd66f6263bde330b052cb2f', '876', 9, 'BF-407102433-DK', 'GOTOWA_DO_ODBIORU'),
(40, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '337', 6, 'PK-686493893-VN', 'ODEBRANA_PRZEZ_KURIERA'),
(41, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '066', 2, 'VG-815536843-IT', 'PRZYGOTOWANIE_DO_NADANIA'),
(42, '5fd66f6263bde330b052cb2d', '5fd66f6263bde330b052cb2f', '046', 10, 'PI-143365765-SE', 'W_TRASNPORCIE'),
(43, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '324', 4, 'ZV-775178880-AU', 'W_TRASNPORCIE'),
(44, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '945', 1, 'EC-686493902-DK', 'ODEBRANA_OD_KURIERA'),
(45, '5fd66f6263bde330b052cb2d', '5fd66f6263bde330b052cb2f', '399', 7, 'DO-540784441-ES', 'GOTOWA_DO_ODBIORU'),
(46, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '769', 2, 'UL-629469437-SE', 'ODEBRANA_OD_KURIERA'),
(47, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '472', 5, 'EK-540784455-GR', 'PRZYGOTOWANIE_DO_NADANIA'),
(48, '5fd66f6263bde330b052cb2d', '5fd66f6263bde330b052cb2f', '990', 6, 'LB-775178893-DK', 'ODEBRANA_OD_KURIERA'),
(49, '5fd66f6263bde330b052cb2f', '5fd66f6263bde330b052cb2d', '356', 6, 'CE-904221801-VN', 'W_TRASNPORCIE'),
(50, '5fd66f6263bde330b052cb2e', '5fd66f6263bde330b052cb2e', '780', 9, 'VE-815536857-BR', 'ODEBRANA_OD_KURIERA');

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `couriers`
--
ALTER TABLE `couriers`
  ADD PRIMARY KEY (`id`);

--
-- Indeksy dla tabeli `packages`
--
ALTER TABLE `packages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_packages_courier_id` (`id_courier`);

--
-- AUTO_INCREMENT dla zrzuconych tabel
--

--
-- AUTO_INCREMENT dla tabeli `couriers`
--
ALTER TABLE `couriers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT dla tabeli `packages`
--
ALTER TABLE `packages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `packages`
--
ALTER TABLE `packages`
  ADD CONSTRAINT `FK_packages_courier_id` FOREIGN KEY (`id_courier`) REFERENCES `couriers` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
