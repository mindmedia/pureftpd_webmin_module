#!/usr/bin/perl
# Edit inetd Pure-FTPd configuration file

do '../web-lib.pl';
&init_config();

&error_setup($text{'pure-conf_err'});
&ReadParse();

if ($in{'ftpdconf'}) {

		# A new configuration file had been send, save it		
		$in{'ftpdconf'} =~ s/\r//g; # Remove Mac line-endings
		&lock_file($file);
		open(FILE, ">$config{'conf_pureftpd'}");
		print FILE $in{'ftpdconf'};
		close(FILE);
		&unlock_file($file);

}

# Display the form
&header($text{'pure-conf_title'}, undef, "conf", 1, 1, undef, $text{'index_mail'});

# Check if there is CSS styles
if ($config{'conf_pureCSS'}) { print "<STYLE type=\"text/css\">
$config{'conf_pureCSS'}\n</STYLE>\n\n"; }

# If init script specified then build a "restart" button
# then if inetd is required, restart 
if ($config{'init_script'}) { 
$restart = "<input type=submit name=save class=submit value=\"$text{'index_apply'}\">"; 
if ($in{'save'} eq $text{'index_apply'}) { system("$config{'init_script'}");
print "<center><h2>$text{'index_restarted'}</h2></center>\n";} }

# Display the inetd configuration file inside the form
$lines = &read_file_lines("$config{'conf_pureftpd'}");
$lines = join("\n", @{$lines}); print <<EOF;

<hr><form action=pure-conf.cgi method=POST>
<center><table border width=70%>
<tr $tb> <td><b>$text{'pure-conf_header'}</b></td> </tr>
<tr $cb> <td><table width=100%>
<tr> <td valign=top nowrap><b>$text{'pure-conf_ftpwelcome'}</b>
<br><br><input type=submit name=save value="$text{'save'}">
<br>$restart</td>
<td><table border width=100%>
<tr $tb> <td><b>$text{'pure-conf_filecontents'}</b></td></tr>
<tr $cb><td><textarea name=ftpdconf rows=30 cols=90>$lines
</textarea></td></tr></table></td> </tr>
</table></td></tr></table></center></form><hr>

EOF

&footer("", $text{'index_return'});