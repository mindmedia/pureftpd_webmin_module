#!/usr/bin/perl
# View Pure-FTPd users.

do '../web-lib.pl';
&init_config();

print "Refresh: $config{'refresh'}\r\n"
	if ($config{'refresh'});

&header($text{'pure-monitor_title'}, undef, "intro", 1, 1, undef, $text{'index_mail'});

# Check if there is CSS styles set
if ($config{'conf_pureCSS'}) { print "<STYLE type=\"text/css\">
$config{'conf_pureCSS'}\n</STYLE>\n\n"; }


# Check if pure-ftpwho is installed.
if (!-x $config{'conf_pureftpdftpwho'}) {
    print "<p><center><h2>",&text('pureftpdmonitor_conf',
          "$config{'conf_pureftpdftpwho'}",
          "/config.cgi?$module_name"),
          "</h2></center><p><hr>\n";
    &footer("/", $text{'index'});
    exit;
}


# Check for monitoring
open (FIC, "$config{'conf_pureftpdftpwho'} -s|");
@results=<FIC>; close(FIC);

# No connected users for the moment
if(!$results[0]) { print "<center><h1>$text{'pure-monitor_nothing'}
</h1></center><br><br><br>\n\n"; } else {

# Number of connected Pure-FTPd users
$users=@results;
if($users==1){ print "<center><h1>$text{'pure-monitor_one'}</h1>";}
else {printf "<center><h1>$text{'pure-monitor_many'}</h1>",$users;}


# Results: table construction
print <<EOF;
<table width="100%" cellspacing="4" border="2" cellpadding="4"><tr $tb>
<td>$text{'pure-monitor_pid'}</td>
<td>$text{'pure-monitor_acct'}</td>
<td>$text{'pure-monitor_time'}</td>
<td>$text{'pure-monitor_state'}</td>
<td>$text{'pure-monitor_file'}</td>
<td>$text{'pure-monitor_peer'}</td>
<td>$text{'pure-monitor_total'}</td>
<td>$text{'pure-monitor_percent'}</td>
<td>$text{'pure-monitor_bandwidth'}</td>
<td>$text{'pure-monitor_local'}</td></tr>
EOF

# Table construction
foreach $i (@results) {

	# pid|acct|time|state|file|peer|local|port|current|total|%|bandwidth
	local ($pid, $login, $time, $state, $file, $peer, $local,
	$port, $current, $total, $percent, $bandwidth) = split(/\|/, $i);
	if(!$file){ $file = "&nbsp;"; }
    if ($state eq "UL") { $state=$text{'pure-monitor_Uploading'}; }
    elsif ($state eq " DL ") { $state=$text{'pure-monitor_Downloading'}; }
    elsif ($state eq "IDLE") { $state=$text{'pure-monitor_Idle'}; }

    if(int($time/60)<10)
    		{ $ttime="0".int($time/60); } 
    		else { $ttime=int($time/60); }
    if($time-(60*int($time/60))<10)
    		{ $ttime="$ttime:0".($time-(60*int($time/60))); } 
    		else { $ttime="$ttime:".($time-(60*int($time/60))); }
    

	print "<tr valign=\"middle\">
<td>$pid</td><td>$login</td><td>$ttime</td><td>$state</td><td>$file</td><td>$peer</td>
<td>$total</td><td>$percent %</td><td>$bandwidth $text{'pure-monitor_speed'}</td>
<td>$local:$port</td></tr>";

} 

print "</table></center><br><br><br><br>\n\n\n"; }

&footer("", $text{'index_return'});