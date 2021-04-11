[![Build Status](https://www.travis-ci.com/neilnm/skyspy.svg?token=qB79Eso2zUjnaeHhLYBV&branch=main)](https://www.travis-ci.com/neilnm/skyspy) ![Python Versions](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C3.9-blue) ![license](https://img.shields.io/github/license/neilnm/skyspy)

# skyspy
skyspy is a Python3 application meant to run on a Raspberry Pi, that will alert you and display flight information when an aircraft is in your vicinity.

It allows you to define what your "vicinity" is by configuring a geofence through lat/lon coordinates and an altitude below which the aircraft should be.

It achieves this with an ADS-B antenna and by parsing the output of the [dump1090](https://github.com/antirez/dump1090) application. See below for more information on how to achieve this. Not as complicated as it sounds!

## Table of Content
- [Assumptions](#Assumptions)
- [Installation](#Installation)
- [Usage](#Usage)
- [Dependencies](#Dependencies)
- [Support](#Support)
- [License](#License)

## Assumptions

 - You have an ADS-B USB dongle and antenna
	 - I'm using a retired model but this is the new version: [Flight Aware ADS-B USB dongle](https://www.amazon.ca/FlightAware-Pro-Stick-ADS-B-Receiver/dp/B01D1ZAP3C/ref=sr_1_5?dchild=1&keywords=ADS-B&qid=1617558428&sr=8-5)
	 - I'm using a similar [Antenna](https://www.amazon.ca/Bingfu-Magnetic-Aviation-Receiver-Software/dp/B082SH4GFH/ref=sr_1_8?dchild=1&keywords=ADS-B&qid=1617558649&sr=8-8)
	 - There are many guides on how to setup an ADS-B antenna, which aren't as complicated as they sound or look. One resource is the following site: [opensky-network.org](https://opensky-network.org/contribute/get-a-receiver)
 - You are running a [Raspberry Pi OS with desktop and recommended software](https://www.raspberrypi.org/software/operating-systems/) and capable of opening a browser. I personally recommend the Raspberry Pi 4 with 4GB of RAM

## Installation

**IMPORTANT**
- There is a bug with one of the os libraries used by [dump1090](https://github.com/antirez/dump1090), see
   [dump1090 issue #142](https://github.com/antirez/dump1090/issues/142)
- Make sure to follow the installation instructions below to workaround this issue.


### Installation Steps
 1. Clone this repository:
	```bash
	git clone https://github.com/neilnm/skyspy.git
	```
 2. Either run the `install.sh` script, which will:
    1. Install [dump1090](https://github.com/antirez/dump1090) by cloning the git repo
	2. Install the OS dependencies using `apt-get`
	3. Install python dependencies using pip

	```bash
	sudo install.sh
	```

	Or install the list of [Dependencies](#Dependencies) yourself and then continue with the steps below in order to fix the bug mentioned above.
&nbsp;

 3. To fix the bug mentioned above, add the following lines to this file:  `/usr/lib/arm-linux-gnueabihf/pkgconfig/librtlsdr.pc`
&nbsp;
	 **Note**: This step is specifically for a Raspbian OS see [dump1090 issue #142](https://github.com/antirez/dump1090/issues/142) if you are running this on a different OS/architecture.


	 ```bash
	prefix=/usr
	exec_prefix=${prefix}
	libdir=${exec_prefix}/lib
	includedir=${prefix}/include
	 ```

	**Note**: After running the install script from step 2, your skyspy directory should have the dump1090 directory within it. Your skyspy directory should look like this:
	```bash
	pi@pi:$HOME/skyspy $ ls -l
	rwxrwxrwx 1 pi pi 324K Apr 3 18:44 alarm.wav
	drwxrwxrwx 5 pi pi 4.0K Apr 3 18:43 dump1090
	-rwxrwxrwx 1 pi pi 631 Apr 4 12:58 install.sh
	drwxrwxrwx 2 pi pi 4.0K Apr 3 18:44 logs
	-rwxrwxrwx 1 pi pi 2.0K Apr 4 12:54 README.md
	-rwxrwxrwx 1 pi pi 209 Apr 3 18:44 skyspy.cfg
	-rwxrwxrwx 1 pi pi 3.6K Apr 3 18:46 skyspy.py
	-rwxrwxrwx 1 pi pi 78 Apr 3 18:46 skyspy_requirements.txt
	drwxrwxrwx 3 pi pi 4.0K Apr 3 18:46 skyutils
	drwxrwxrwx 2 pi pi 4.0K Apr 3 18:46 web
	```

 4. Go to the dump1090 directory and run `make`:
	```bash
	cd dump1090
	sudo make
	```
 5. Grab a cup of :coffee:, you are ready to use skyspy :smile:


## Usage

 1. Setup the `skyspy.cfg` config file:

	1. [GEO_FENCE] -- skyspy will alert you if a plane is within a certain geofence/zone using lat/lon coordinates. I used this tool to determine the 	zone: https://www.keene.edu/campus/maps/tool/ or https://www.doogal.co.uk/polylines.php Once you have the coordinates, enter them under [GEO_FENCE].
	2.  [HOME] -- If multiple planes are within a zone, skyspy will use the home point to determine the closest one to display. Enter your home coordinates under [HOME]
	3. [AIRPORT] -- skyspy will use the airport and runway entered in the config file to pull the METAR/weather information for that airport and display the most likely runway in use based on the runway entered in the config file. Enter the 4 letter ICAO aiport code under `[AIRPORT] -> station ` and the runway under `[AIRPORT] -> runway.`
&nbsp;

	**IMPORTANT**
	Make sure there are no spaces between your coordinates. Your config file should look like the example below:

	 ```bash
	[GEO_FENCE]
	p1 = 37.629562,-116.849556
	p2 = 37.649562,-116.849556
	p3 = 37.649562,-116.829556
	p4 = 37.629562,-116.829556

	[HOME]
	p1 = 37.629562,-116.849556

	[ALTITUDE]
	alt = 5000

	[AIRPORT]
	station = CYUL
	runway = 24
	```


2. Run skyspy
	From your skyspy directory, run the following command:
	```bash
	python3 skyspy.py
	```

3. If everything has been setup correctly, skyspy will open in a new tab and also display the raw output of [dump1090](https://github.com/antirez/dump1090) on the terminal

	 - terminal <br>
![term](https://i.ibb.co/ZVXLFsJ/term.jpg)

	 - skyspy at startup
![wo-info](https://i.ibb.co/yBjwtdj/skyspy-wo-info.jpg)

	 - skyspy displaying a plane
![w-info](https://i.ibb.co/sRsKDXt/skyspy-w-info.jpg)
&nbsp;

4. If you wish to change the sound of the alert, simply overwrite the `alarm.wav` in the `skyspy` directory with your favourite sound.

## Dependencies

**Note**: The install script will do this for you. If you have already ran the install script, ignore this section.

Missing dependencies based on Raspbian system:

- Software
	 - [dump1090](https://github.com/antirez/dump1090) which should be installed within the `skyspy` directory
 - Operating System dependencies which can be installed via `apt-get`:
	 - `librtlsdr-dev`
	 - `libgeos-dev`
 - Python dependencies which can be installed using `python3 -m pip`:
	 - `shapely`

## Support

If you have any questions or issues, feel free to open an issue or to reach me by email and I will try to answer when I can.

## License

[MIT](https://choosealicense.com/licenses/mit/)
