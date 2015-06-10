#!/usr/bin/python
# -*- coding: utf-8 -*-

import bint as lib
import sys
import random


def miller_rabin_pass(a, s, d, n):
	a_to_power = pow(a, d, n)

	if a_to_power == 1:
		return True

	for i in xrange(s - 1):
		if a_to_power == n - 1:
			return True
		a_to_power = (a_to_power * a_to_power) % n

	return a_to_power == n - 1


def miller_rabin(n):
	"""Тест Миллера-Рабина на простоту числа

	"""
	n = n.st()
	n = int(n)

	d = n - 1
	s = 0

	while d % 2 == 0:
		d >>= 1
		s += 1

	for repeat in xrange(20):
		a = 0

		while a == 0:
			a = random.randrange(n)
		if not miller_rabin_pass(a, s, d, n):
			return False

	return True


def prime_test(num):
	if not miller_rabin(num):
		raise ValueError("Выбранное число не является простым.")


def xgcd(a, b):
	"""Расширенный алгоритм Евклида

	"""
	if a == lib.bint(0):
		return 0, 1, b

	if b == lib.bint(0):
		return 1, 0, a

	px = lib.bint(0)
	ppx = lib.bint(1)
	py = lib.bint(1)
	ppy = lib.bint(0)

	while b > lib.bint(0):
		q = a / b
		a, b = b, a % b
		x = ppx - q * px
		y = ppy - q * py
		ppx, px = px, x
		ppy, py = py, y

	return ppx, ppy, a


def generate_d(a, b):
	"""Генерирует число d

	"""
	while True:
		x, y, g = xgcd(a, b)

		if g != lib.bint(1):
			raise ValueError("Невозможно подобрать такое d, чтобы выполнялось условие d * e mod fi = 1.")
		else:
			z = x % b
			break
	return z


def rsa(msg, p, q, e):

	msg = lib.bint(str(msg))

	modulus = p * q

	fi = (p - lib.bint(1)) * (q - lib.bint(1))

	if msg > modulus:
		raise ValueError("Неверная длина сообщения")

	d = generate_d(e, fi)

	ciphertext = d.powmod(msg, e, modulus)                      # Кодирование

	decode_msg = d.powmod(ciphertext, d, modulus)               # Декодирование

	return decode_msg


def usage():
	print "\nИспользование: python RSA.py msg.txt\n"

	sys.exit(-1)


if __name__ == "__main__":
	if len(sys.argv) != 2:
		usage()

	f = open(sys.argv[1])

	msg = int(f.read())

	f.close()

	tmp = lib.bint()

	p = lib.bint(tmp.read("p.txt"))
	q = lib.bint(tmp.read("q.txt"))
	e = lib.bint(tmp.read("e.txt"))

	prime_test(p)
	prime_test(q)
	prime_test(e)

	decode_msg = rsa(msg, p, q, e)

	f = open("decode_msg.txt", "w")

	f.write(decode_msg.st())

	f.close()
