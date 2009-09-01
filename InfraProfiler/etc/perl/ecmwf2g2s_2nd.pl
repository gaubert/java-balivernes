
eval 'exec ${PERLPATH}perl $0 ${1+"$@"}'
if 0;
$HOME       = $ENV{HOME};
$CMS_CONFIG = $ENV{'CMS_CONFIG'};


# ########################################################################################
#
# File: Extraction of ECMWF data, merging with HWM07/MSISE00 and creation of
#	G2SGCS-bin.
#
# Usage: fill in "input_ecmwf2g2s_case.par"  and run ecmwf2g2s_2nd.pl 
#
# Author: P.Mialle
# Last updated: April 2009 (updated August 2009)
#
# ########################################################################################

use POSIX;

# output files
$basedir	= "/home/smd/aubert/public/infrasound/g2s_bin_generator/retrieveG2S";
$workdir    	= "$basedir/extractG2SECMWF";
$e2hdir     	= "$CMS_CONFIG/../rel/bin";
$ECMWF_archive 	= "/archive/ops/atm/Metdata/ECMWF";
$ECMWF_ops 	= "/ops/data/atm/primary-met";
$input_file 	= "input_ecmwf2g2s_case.par";
$g2smodel_dir	= "$workdir";
$g2smodel	= "g2smodel4.1.gfort";
$NOAA_logfile	= "ftpNOAA.log";
$ftpNOAA_dir	= "$workdir";
$output_dir	= "/archive/projects/sm/projects/Infraref/G2SECMWF";
$logdir		= "$workdir/log";


# Input file
open(FILEH, $input_file) || die("Could not open the file!");
my @input = <FILEH>;
close(FILEH);


# Check the available data in ops-dir
@flines = `ls $ECMWF_ops/EN????????`;

$ind = 0;
foreach (@flines)
{
	@fdates = split(/EN/,$_);
	$curdate = $fdates[1];
	if($curdate[0] == '0')
	{
		$curdate = "20".$curdate;
	}
	else
	{
		$curdate = "19".$curdate;
	}
	$alldate[$ind] = `h2e ofmt="%#" $curdate `;
	chomp($alldate[$ind]);
	$ind++;
}

@alldate = sort { $a <=> $b } @alldate;
my $mintime = $alldate[0];
@alldate = reverse sort { $a <=> $b } @alldate;
my $maxtime = $alldate[0];


# Loop over all needed dates
foreach (@input)
{
	# Split all information from the current date
	chomp($_);
	@curdate_tmp = split(/ /,$_);
	$curdate = `h2e ofmt="%#" $curdate_tmp[0] $curdate_tmp[1]`;
	chomp($curdate);

	$YYYY	= substr($curdate_tmp[0],0,4);
	$YY	= substr($curdate_tmp[0],2,2);
	$MM	= substr($curdate_tmp[0],5,2);
	$DD	= substr($curdate_tmp[0],8,2);
	$HH	= substr($curdate_tmp[1],0,2);
	$mnmn	= substr($curdate_tmp[1],3,2);
	printf STDOUT "YYYY=%s Full=%s-%s-%s %s:%s\n",$YYYY,$YY,$MM,$DD,$HH,$mnmn;

	# Prepare the G2S output directory
	`mkdir -p $output_dir/$YYYY$MM`;

	# Retrieve geomatric and solar indices
	`$ftpNOAA_dir/ftpNOAA_pk.pl date=$YYYY$MM$DD >& $logdir/$NOAA_logfile`;

	open(FILEH2,"$logdir/$NOAA_logfile") || die("Could not open the file!");
	@RSGA = <FILEH2>;
	chomp(@RSGA);
	close(FILEH);

	$F107  = $RSGA[0];
	$F107a = $RSGA[1];
	$Ap    = $RSGA[2];
	printf STDOUT "F107=%s F107a=%s Ap=%s\n",$F107,$F107a,$Ap;

#	my $HHrnd = sprintf("%.0f",($HH+$mnmn/60)/3);	# Closest 3h-time
#	$HHrnd = $HHrnd*3;
	my $HHrnd = ceil(($HH+$mnmn/60)/3)*3;
#	printf STDOUT "HHrnd=%d (HH=%d mnmn=%d)\n",$HHrnd,$HH,$mnmn;
	if ($HHrnd < 10)
	{
		$HHrnd = "0".$HHrnd;
	}
	elsif ($HHrnd == 24)
	{
		$HHrnd = 21;
		# should be updated to take the midnight data from next day and increment if needed the month and year)
	}
	

	$ENfilename = "EN"."$YY$MM$DD$HHrnd";
	printf STDOUT "HHrnd=%d(%s) ENname=%s\n",$HHrnd,$HHrnd,$ENfilename;

	# Execute g2smodel to build the G2SGCSx....bin file containing all G2S atmospheric caracteristics
	$g2s_logfile = "g2s"."$YYYY$MM$DD$mnmn.log";
	printf STDOUT "curdate=%s > mintime=%s ? (Y=Ops N=archive)\n",$curdate,$mintime;
	if($curdate > $mintime)
	{
		# EN-files are in Ops-directory
		printf STDOUT "$g2smodel_dir/$g2smodel -v -d $output_dir/$YYYY$MM -i $F107 $F107a $Ap $ECMWF_ops/$ENfilename >& $logdir/$g2s_logfile\n";
		`$g2smodel_dir/$g2smodel -v -d $output_dir/$YYYY$MM -i $F107 $F107a $Ap $ECMWF_ops/$ENfilename >& $logdir/$g2s_logfile`;
	}
	else
	{
		# EN-files are in Archive-directory
		printf STDOUT "$g2smodel_dir/$g2smodel -v -d $output_dir/$YYYY$MM -i $F107 $F107a $Ap $ECMWF_archive/$YYYY$MM/$ENfilename >& $logdir/$g2s_logfile\n";
		`$g2smodel_dir/$g2smodel -v -d $output_dir/$YYYY$MM -i $F107 $F107a $Ap $ECMWF_archive/$YYYY$MM/$ENfilename >& $logdir/$g2s_logfile`;
	}

}

exit;
