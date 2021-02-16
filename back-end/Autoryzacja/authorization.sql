-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Czas generowania: 11 Lut 2021, 20:27
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
-- Baza danych: `authorization`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `accounts`
--

CREATE TABLE `accounts` (
  `id` int(11) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `login` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `library_id` int(11) NOT NULL,
  `address` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `zip_code` varchar(255) NOT NULL,
  `date_created` datetime NOT NULL,
  `account_type` enum('READER','EMPLOYEE') NOT NULL,
  `email` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Zrzut danych tabeli `accounts`
--

INSERT INTO `accounts` (`id`, `first_name`, `last_name`, `login`, `password`, `library_id`, `address`, `city`, `zip_code`, `date_created`, `account_type`, `email`) VALUES
(1, 'Wojciech', 'Wrona', 'admin', 'pbkdf2:sha256:150000$wbkqgCQi$af07e718e970850216828ea75aa5e09d9212458945e9349dbed2f359a3002d52', 1, 'aleja Tadeusza Rejtana 16C, 35-310 Rzeszów', 'Rzeszów', '35-310', '2021-02-11 20:15:42', 'EMPLOYEE', 'wojtekwrona232@gmail.com');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `libraries`
--

CREATE TABLE `libraries` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `address` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Zrzut danych tabeli `libraries`
--

INSERT INTO `libraries` (`id`, `name`, `address`, `city`) VALUES
(1, 'Wojewódzka i Miejska Biblioteka Publiczna w Rzeszo', 'Sokoła 13, 35-010 Rzeszów', 'Rzeszów'),
(2, 'Miejska Biblioteka Publiczna w Łańcucie', 'Moniuszki 2, 37-100 Łańcut', 'Łańcut');

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_accounts_library_id` (`library_id`);

--
-- Indeksy dla tabeli `libraries`
--
ALTER TABLE `libraries`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT dla zrzuconych tabel
--

--
-- AUTO_INCREMENT dla tabeli `accounts`
--
ALTER TABLE `accounts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT dla tabeli `libraries`
--
ALTER TABLE `libraries`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `accounts`
--
ALTER TABLE `accounts`
  ADD CONSTRAINT `FK_accounts_library_id` FOREIGN KEY (`library_id`) REFERENCES `libraries` (`id`) ON DELETE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
