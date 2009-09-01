
eval 'exec ${PERLPATH}perl $0 ${1+"$@"}'
if 0;
$HOME       = $ENV{HOME};
$CMS_CONFIG = $ENV{'CMS_CONFIG'};
require "getpar.pl";


# ########################################################################################
#
# File: ftpNOAA.pl
#
# Description:
# Script that automatically connects to NOAA website and retrieves the solar flux (f10.7)
# and Geomagnetic Ap indices for specified day
# F10.7 and Ap values are used by infraMAP and G2Smodel software.
#
# Usage:
# ftpNOAA.pl date=<YYYYMMDD>
#
# Author: N.Brachet PTS/IDC
# Last updated: Feb 2007
#
# ########################################################################################


# output files
$workdir    = "$HOME/Workplace_Pk/retrieveG2S/";
$file_err   = "$workdir/error.log";
$bindir     = "/opt/OSS/bin";
$e2hdir     = "$CMS_CONFIG/../rel/bin";
#$archivedir = "$workdir/RSGA_Archive";
#$archivedir = "/home/smd/brachet/ftpNOAA/RSGA_Archive";
$archivedir = "/dvlscratch/SHI/mialle/SWPC";

%par = getpar(@ARGV);

if ($par{'date'})
{
	$ReqDate = $par{'date'};
}
else
{
	warn "**** Error ***** Usage: ftpNOAA.pl date=<YYYYMMDD>\n";
	exit;
}

$ReqDay_ep = `$e2hdir/h2e ofmt="%#" $ReqDate`;
$ReqYYYY   = substr($ReqDate,0,4);
$ReqMMDD   = substr($ReqDate,4,4);
$ReqYY     = substr($ReqDate,2,2);
$ReqMM     = substr($ReqDate,4,2);
$ReqDD     = substr($ReqDate,6,2);

# Basic check of the requested date
$today     = `h2e today ofmt=%#`;
$DateDiff  = ($today-$ReqDay_ep)/86400;
if (($DateDiff < 0) || ($ReqDay_ep < 820540800))
{
	printf STDOUT "ERROR: the requested date must be between January 2,1996 and today\n";
	exit;
}


# The previous day is supposed to give better estimate of the indices than the current day
#
$previousday = $ReqDay_ep-86400;
@gmdate = gmtime($previousday);
$YYYYMMDD = sprintf("%04s%02s%02s",1900+$gmdate[5],$gmdate[4]+1,$gmdate[3]);
$YYYY     = substr($YYYYMMDD,0,4);
$filename = sprintf("%8sRSGA.txt",$YYYYMMDD);


if ($YYYY >= 2009)
{
	# --- Use the website for the most recent indices
	#
	ftpNOAArealtime($bindir,$workdir,$file_err,$filename,$ReqDay_ep);
	
	# --- Read the indices from the downloaded file
	#
	($f107, $f107a, $Ap) = extractIndices($workdir,$filename);
	`rm $workdir/$filename $file_err`;
	
#	printf STDOUT "\n10.7cm solar flux\n";
	printf STDOUT "%d\n",$f107;
	printf STDOUT "%d\n",$f107a;
#	printf STDOUT "\nGeomagnetic Indice\n";
	printf STDOUT "%d\n",$Ap;

#	printf STDOUT "command line: g2smodel91 -v -d . -i %d %d %d  /ops/data/atm/primary-met/EN%02d%02d%02d{hh}\n",
#		$f107,$f107a,$Ap,${ReqYY},${ReqMM},${ReqDD};

}
else
{
	# Use the indices from our archive
	#
#	$fluxfile = sprintf("%s/%s/%s",$archivedir,$YYYY,$filename);
	$archivetmp = sprintf("%s/%s/RSGA",$archivedir,$YYYY);
#	printf STDOUT "\nRetrieving data from archive:\n";
#	printf STDOUT "%s\n",$fluxfile;
	
	# --- Read the indices from archive file
	#
#	($f107, $f107a, $Ap) = extractIndices($fluxfile);
	($f107, $f107a, $Ap) = extractIndices($archivetmp,$filename);
	
#	printf STDOUT "\n10.7cm solar flux\n";
	printf STDOUT "%d\n",$f107;
	printf STDOUT "%d\n",$f107a;
#	printf STDOUT "\nGeomagnetic Indice\n";
	printf STDOUT "%d\n",$Ap;

#	printf STDOUT "command line: g2smodel91 -v -d . -i %d %d %d  /archive/ops/atm/Metdata/ECMWF/%04d%02d/EN%02d%02d%02d{hh}\n",
#		$f107,$f107a,$Ap,${ReqYYYY},${ReqMM},${ReqYY},${ReqMM},${ReqDD};

}


exit;




###################################################################################################


sub ftpNOAArealtime()
{
my ($bindir,$workdir,$file_err,$filename) = @_;

	# $httpfile = sprintf("http://www.sec.noaa.gov/ftpdir/warehouse/%s/RSGA/%s",$YYYY,$filename);
        $httpfile = sprintf("http://www.swpc.noaa.gov/ftpdir/warehouse/%s/RSGA/%s",$YYYY,$filename);
#	printf STDOUT "\nRetrieving real time data from NOAA ftp site (file for previous day):\n";
#	printf STDOUT "%s\n",$httpfile;
	
	#`$bindir/wget $httpfile -O $workdir/$filename 1>$file_err 2>&1`;
        `wget $httpfile -O $workdir/$filename 1>$file_err 2>&1`;
}


###################################################################################################


sub extractIndices()
{
my ($workdir,$fluxfile) = @_;
my $filename;
	my $block4, $line, $f107, $f107a, $Ap;

	# Extract F10.7 and Ap from the dowloaded file
	#
	$filename = "$workdir/$fluxfile";
#	printf STDOUT "\nFile: %s\n",$filename;
#	printf STDOUT "\nWorkdir: %s FluxF:%s\n",$workdir,$fluxfile;
	
	open (INPUTFILE, $filename) || die "NOAA File not found";
	$block4 = 0;
	foreach $line (<INPUTFILE>)
	{
		$_ = $line;
		if (/^IV./)
		{
			$block4 = 1;
			next;
		}
		if (($block4 == 1) && (/Observed|OBSERVED/))
		{
			# Read f10.7 indice from block IV.
			$_ = $line;
			@field = split;
			$f107 = $field[3];
			$block4 = 2;
			next;
		}
		if (/^90 Day Mean|^90 DAY MEAN/)
		{
			# Read f10.7a indice
			$_ = $line;
			@field = split;
			$f107a = $field[5];
			next;
		}
		if (/^Observed Afr\/Ap|^OBSERVED AFR\/AP|^OBSERVED  AFR\/AP/)
		{
			# Read Ap indice
			$_ = $line;
			@field = split;
			$Ap = substr($field[4],4,3);
			last;
		}
	}
	return ($f107,$f107a,$Ap);
}
