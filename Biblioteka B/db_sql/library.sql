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
-- Baza danych: `library`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `isbn` varchar(255) NOT NULL,
  `available` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Zrzut danych tabeli `books`
--

INSERT INTO `books` (`id`, `isbn`, `available`) VALUES
(1, '971-417-906-8', 1),
(2, '9268-5-2105-9', 1),
(3, '971-417-906-8', 1),
(4, '971-417-906-8', 0),
(5, '9268-5-2105-9', 0),
(6, '971-417-906-8', 1),
(7, '971-417-906-8', 1);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `check_outs`
--

CREATE TABLE `check_outs` (
  `id` int(11) NOT NULL,
  `reservation_id` int(11) DEFAULT NULL,
  `book_id` int(11) NOT NULL,
  `reader_id` varchar(255) NOT NULL,
  `employee_id` varchar(255) NOT NULL,
  `check_out_date` date DEFAULT NULL,
  `return_date` date DEFAULT NULL,
  `return_term` date DEFAULT NULL,
  `late_return_penalty` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Zrzut danych tabeli `check_outs`
--

INSERT INTO `check_outs` (`id`, `reservation_id`, `book_id`, `reader_id`, `employee_id`, `check_out_date`, `return_date`, `return_term`, `late_return_penalty`) VALUES
(2, NULL, 5, 'wojtek232', 'jan.kowalski@example.com', '2021-01-07', NULL, '2021-01-28', 0);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `reservations`
--

CREATE TABLE `reservations` (
  `id` int(11) NOT NULL,
  `reservation_date` date NOT NULL,
  `pick_up_date` date NOT NULL,
  `status` enum('W_REALIZACJI','W_TRANSPORCIE','GOTOWA_DO_ODBIORU','ANULOWANO','ODEBRANO') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Zrzut danych tabeli `reservations`
--

INSERT INTO `reservations` (`id`, `reservation_date`, `pick_up_date`, `status`) VALUES
(1, '2021-01-06', '2021-01-11', 'W_REALIZACJI'),
(3, '2020-01-19', '2020-01-21', 'GOTOWA_DO_ODBIORU');

--
-- Indeksy dla zrzutów tabel
--

--
-- Indeksy dla tabeli `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);

--
-- Indeksy dla tabeli `check_outs`
--
ALTER TABLE `check_outs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_check_outs_book_id` (`book_id`),
  ADD KEY `FK_check_outs_reservation_id` (`reservation_id`);

--
-- Indeksy dla tabeli `reservations`
--
ALTER TABLE `reservations`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT dla zrzuconych tabel
--

--
-- AUTO_INCREMENT dla tabeli `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT dla tabeli `check_outs`
--
ALTER TABLE `check_outs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT dla tabeli `reservations`
--
ALTER TABLE `reservations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `check_outs`
--
ALTER TABLE `check_outs`
  ADD CONSTRAINT `FK_check_outs_book_id` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE NO ACTION,
  ADD CONSTRAINT `FK_check_outs_reservation_id` FOREIGN KEY (`reservation_id`) REFERENCES `reservations` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
