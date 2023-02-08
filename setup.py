"""
Copyright (C) 2023  Miles Rack

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from setuptools import setup

setup(
	author="Miles Rack",
	description="A blockchain implementation for the \"Cybercoin\" (CYB) cryptocurrency at CBCYBER.",
	name="cybercoin",
	version="0.1.0",
	url="https://github.com/milesrack/cybercoin",
	packages=["cybercoin"],
	install_requires=[
		"requests >= 2.28.1",
		"pycryptodome >= 3.17"
	],
)
