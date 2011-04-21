#!/usr/bin/perl
# Edit Pure-FTPd users.

do '../web-lib.pl';
&init_config(); &ReadParse();

&header($text{'pure-users_title'}, undef, "users", 1, 1, undef, $text{'index_mail'});


# Check if there is CSS styles
if ($config{'conf_pureCSS'}) { print "<STYLE type=\"text/css\">
$config{'conf_pureCSS'}\n</STYLE>\n\n"; }

# Check if pure-pw is installed.
if (!-x $config{'conf_pureftpdpw'}) {
    print "<p><hr><center><h2>",
          &text('pure-users_conf',
                "<tt>$config{'conf_pureftpdpw'}</tt>",
                "/config.cgi?$module_name"),
          "</h2></center><p>\n<hr>\n";
    &footer("/", $text{'index'});
    exit;
}


sub Pureparse() {
	$action .= "-u \"$in{'uid'}\" -g \"$in{'gid'}\" -c \"$in{'gecos'}\" ".
	"$in{'chroot'} \"$in{'home'}\" -T \"$in{'upload_band'}\" ".
	"-t \"$in{'download_band'}\" -q \"$in{'upload_ratio'}\" ".
	"-Q \"$in{'download_ratio'}\" -y \"$in{'max_sessions'}\" ".
	"-z \"$in{'time'}\" -y \"$in{'max_sessions'}\" ".
	"-n \"$in{'max_files'}\" -N \"$in{'max_size'}\" ".
	"-i \"$in{'allow_local_IP'}\" -I \"$in{'deny_local_IP'}\" ".
	"-r \"$in{'allow_client_IP'}\" -R \"$in{'deny_client_IP'}\" ";
}


sub sort_as_wanted {

	# retrieve sort preferences
	if($in{'sort'} ne "") { $sort=$in{'sort'}; }else{ $sort=$config{'conf_sort'}; }

	
	# retrieve User 1 informations
	local ($logina, $passwd, $uida, $gida, $gecosa, $homea,
	$upload_band, $download_band, $upload_ratio, $download_ratio,
	$max_sessions, $max_files, $max_size, 
	$allow_local_IP, $deny_local_IP, 
	$allow_client_IP, $deny_client_IP, $time) = split(/:/,$a);

	# retrieve User 2 informations
	local ($loginb, $passwd, $uidb, $gidb, $gecosb, $homeb,
	$upload_band, $download_band, $upload_ratio, $download_ratio,
	$max_sessions, $max_files, $max_size, 
	$allow_local_IP, $deny_local_IP, 
	$allow_client_IP, $deny_client_IP, $time) = split(/:/,$b);
	
	# Then compare to match the sort preferences

	   if($sort eq "uid") {      "\U$uida"   cmp "\U$uidb" 
                              || "\U$logina" cmp "\U$loginb" }
	elsif($sort eq "gecos") {    "\U$gecosa" cmp "\U$gecosb" 
                              || "\U$logina" cmp "\U$loginb" }
	elsif($sort eq "home") {     "\U$homea"  cmp "\U$homeb" 
                              || "\U$logina" cmp "\U$loginb" }
	elsif($sort eq "gid") {      "\U$gida"   cmp "\U$gidb" 
                              || "\U$uida"   cmp "\U$uidb"
                              || "\U$logina" cmp "\U$loginb" }

	                      # Otherwise, sort by login
	                      else { "\U$logina" cmp "\U$loginb" }
	 
}

sub Newuser() {
	$action .= "-u $in{'uid'} -g $in{'gid'} ".
	"-c \"$in{'gecos'}\" $in{'chroot'} \"$in{'home'}\" ";
	
	# Parse the new user's information
	if($in{'allow_local_IP'}) 	{ $action .= "-i \"$in{'allow_local_IP'}\" "; }
	if($in{'deny_local_IP'}) 	{ $action .= "-I \"$in{'deny_local_IP'}\" "; }
	if($in{'max_files'}) 		{ $action .= "-n \"$in{'max_files'}\" "; }
	if($in{'max_size'}) 		{ $action .= "-N \"$in{'max_size'}\" "; }
	if($in{'upload_ratio'}) 	{ $action .= "-q \"$in{'upload_ratio'}\" "; }
	if($in{'download_ratio'}) 	{ $action .= "-Q \"$in{'download_ratio'}\" "; }
	if($in{'allow_client_IP'}) 	{ $action .= "-r \"$in{'allow_client_IP'}\" "; }
	if($in{'deny_client_IP'}) 	{ $action .= "-R \"$in{'deny_client_IP'}\" "; }
	if($in{'upload_band'}) 		{ $action .= "-T \"$in{'upload_band'}\" "; }
	if($in{'download_band'}) 	{ $action .= "-t \"$in{'download_band'}\" "; }
	if($in{'max_sessions'}) 	{ $action .= "-y \"$in{'max_sessions'}\" "; }
	if($in{'time'}) 			{ $action .= "-z \"$in{'time'}\" "; }
}


sub Setdisplay() { # Subroutine to parse, change and set users display

	# Check if form sent to overide configuration preferences
       if($in{'d_login'} eq "0") {   $config{'conf_displaylogin'} = ""; $displ{'login'}=1;}
    elsif($in{'d_login'} ne "") {    $config{'conf_displaylogin'} = $in{'d_login'}; $displ{'login'}=1;}
    elsif($config{'conf_displaylogin'}  ne "") { $displ{'login'}=1;}

       if($in{'d_gecos'} eq "0") {   $config{'conf_displaygecos'} = ""; $displ{'gecos'}=1; }
    elsif($in{'d_gecos'} ne "") {    $config{'conf_displaygecos'} = $in{'d_gecos'}; $displ{'gecos'}=1; }
    elsif($config{'conf_displaygecos'}  ne "") { $displ{'gecos'}=1;}

       if($in{'d_home'} eq "0") {    $config{'conf_displayhome'}  = ""; $displ{'home'}=1; }
    elsif($in{'d_home'} ne "") {     $config{'conf_displayhome'}  = $in{'d_home'}; $displ{'home'}=1; }
    elsif($config{'conf_displayhome'}  ne "") { $displ{'login'}=1;}

       if($in{'d_uid'} eq "0") {     $config{'conf_displayuid'}   = ""; $displ{'uid'}=1; }
    elsif($in{'d_uid'} ne "") {      $config{'conf_displayuid'}   = $in{'d_uid'}; $displ{'uid'}=1; }
    elsif($config{'conf_displayuid'}  ne "") { $displ{'uid'}=1;}

       if($in{'d_gid'} eq "0") {     $config{'conf_displaygid'} = ""; $displ{'gid'}=1; }
    elsif($in{'d_gid'} ne "") {      $config{'conf_displaygid'} = $in{'d_gid'}; $displ{'gid'}=1; }
    elsif($config{'conf_displaygid'}  ne "") { $displ{'gid'}=1;}

       if($in{'d_upband'} eq "0") {  $config{'conf_displayupband'} = ""; $displ{'upband'}=1; }
    elsif($in{'d_upband'} ne "") {   $config{'conf_displayupband'} = $in{'d_upband'}; $displ{'upband'}=1; }
    elsif($config{'conf_displayupband'}  ne "") { $displ{'upband'}=1;}

       if($in{'d_dwband'} eq "0") {  $config{'conf_displaydwband'} = ""; $displ{'dwband'}=1; }
    elsif($in{'d_dwband'} ne "") {   $config{'conf_displaydwband'} = $in{'d_dwband'}; $displ{'dwband'}=1; }
    elsif($config{'conf_displaydwband'}  ne "") { $displ{'dwband'}=1;}

       if($in{'d_upratio'} eq "0") { $config{'conf_displayupratio'} = ""; $displ{'upratio'}=1; }
    elsif($in{'d_upratio'} ne "") {  $config{'conf_displayupratio'} = $in{'d_upratio'}; $displ{'upratio'}=1; }
    elsif($config{'conf_displayupratio'}  ne "") { $displ{'upratio'}=1;}

       if($in{'d_dwratio'} eq "0") { $config{'conf_displaydwratio'} = ""; $displ{'dwratio'}=1; }
    elsif($in{'d_dwratio'} ne "") {  $config{'conf_displaydwratio'} = $in{'d_dwratio'}; $displ{'dwratio'}=1; }
    elsif($config{'conf_displaydwratio'}  ne "") { $displ{'dwratio'}=1;}

       if($in{'d_mxfile'} eq "0") {  $config{'conf_displaymxfile'} = ""; $displ{'mxfile'}=1; }
    elsif($in{'d_mxfile'} ne "") {   $config{'conf_displaymxfile'} = $in{'d_mxfile'}; $displ{'mxfile'}=1; }
    elsif($config{'conf_displaymxfile'}  ne "") { $displ{'mxfile'}=1;}

       if($in{'d_mxsize'} eq "0") {  $config{'conf_displaymxsize'} = ""; $displ{'mxsize'}=1; }
    elsif($in{'d_mxsize'} ne "") {   $config{'conf_displaymxsize'} = $in{'d_mxsize'}; $displ{'mxsize'}=1; }
    elsif($config{'conf_displaymxsize'}  ne "") { $displ{'mxsize'}=1;}

       if($in{'d_percfile'} eq "0"){ $config{'conf_displaypercfile'} = ""; $displ{'percfile'}=1; }
    elsif($in{'d_percfile'} ne "") { $config{'conf_displaypercfile'} = $in{'d_percfile'}; $displ{'percfile'}=1; }
    elsif($config{'conf_displaypercfile'}  ne "") { $displ{'percfile'}=1;}

       if($in{'d_percsize'} eq "0"){ $config{'conf_displaypercsize'} = ""; $displ{'percsize'}=1; }
    elsif($in{'d_percsize'} ne "") { $config{'conf_displaypercsize'} = $in{'d_percsize'}; $displ{'percsize'}=1; }
    elsif($config{'conf_displaypercsize'}  ne "") { $displ{'percsize'}=1;}

       if($in{'d_sess'} eq "0") {    $config{'conf_displaysession'} = ""; $displ{'session'}=1; }
    elsif($in{'d_sess'} ne "") {     $config{'conf_displaysession'} = $in{'d_sess'}; $displ{'session'}=1; }
    elsif($config{'conf_displaysession'}  ne "") { $displ{'session'}=1;}

       if($in{'d_chroot'} eq "2" ||  $config{'conf_displaychroot'} eq "2") 
                                  {  $config{'conf_displaychroot'} = "2"; $displ{'chroot'}=1; }
    elsif( $in{'d_chroot'} ne "") {  $config{'conf_displaychroot'} = $in{'d_chroot'}; $displ{'chroot'}=1; }
    elsif($config{'conf_displaychroot'} ne "") { $displ{'chroot'}=1;}

	
	# Parse the display configuration preferences
	($minuid,$maxuid) = split(/-/, $config{'conf_displayuid'});
	($mingid,$maxgid) = split(/-/, $config{'conf_displaygid'});
	($minupb,$maxupb) = split(/-/, $config{'conf_displayupband'});
	($mindlb,$maxdlb) = split(/-/, $config{'conf_displaydwband'});
	($minupr,$maxupr) = split(/-/, $config{'conf_displayupratio'});
	($mindlr,$maxdlr) = split(/-/, $config{'conf_displaydwratio'});
	($minfil,$maxfil) = split(/-/, $config{'conf_displaymxfile'});
	($minsiz,$maxsiz) = split(/-/, $config{'conf_displaymxsize'});
	($minprf,$maxprf) = split(/-/, $config{'conf_displaypercfile'});
	($minprs,$maxprs) = split(/-/, $config{'conf_displaypercsize'});
	($minses,$maxses) = split(/-/, $config{'conf_displaysession'});
	

	# Build the display form
	
	# Values with regexp expression
	if($displ{'login'} ne "" || $displ{'gecos'} ne "" || $displ{'home'} ne "") 
	{ $display.= "<br><br><b>".$text{'pure-users_criteriaregexp'}."</b><br>\n"; }
	if($displ{'login'} ne "") {  $display.= " ".$text{'pure-users_criterialogin'}.
	"&nbsp;<input type=text name=d_login size=10 value=\"$config{'conf_displaylogin'}\">\n"; }
	if($displ{'gecos'} ne "") {  $display.= " ".$text{'pure-users_criteriagecos'}.
	"&nbsp;<input type=text name=d_gecos size=10 value=\"$config{'conf_displaygecos'}\">\n"; }
	if($displ{'home'} ne "") {  $display.= " ".$text{'pure-users_criteriahome'}.
	"&nbsp;<input type=text name=d_home size=10 value=\"$config{'conf_displayhome'}\">\n"; }
	
	# Values from 000-000
	if($displ{'uid'} ne ""      || $displ{'gid'} ne ""
	|| $displ{'upband'} ne ""   || $displ{'dwband'} ne ""
	|| $displ{'upratio'} ne ""  || $displ{'dwratio'} ne ""
	|| $displ{'mxfile'} ne ""   || $displ{'mxsize'} ne ""
	|| $displ{'percfile'} ne "" || $displ{'percsize'} ne ""
	|| $displ{'session'} ne "" ) { $display.= "<br><br><b>".$text{'pure-users_criteriavalues'}."</b><br>\n"; }
	if($displ{'uid'} ne "") {  $display.= " ".$text{'pure-users_criteriauid'}.
	"&nbsp;<input type=text name=d_uid size=10 value=\"$config{'conf_displayuid'}\">\n"; }
	if($displ{'gid'} ne "") {  $display.= " ".$text{'pure-users_criteriagid'}.
	"&nbsp;<input type=text name=d_gid size=10 value=\"$config{'conf_displaygid'}\">\n"; }
	if($displ{'upband'} ne "") {  $display.= " ".$text{'pure-users_criteriaupband'}.
	"&nbsp;<input type=text name=d_upband size=10 value=\"$config{'conf_displayupband'}\">\n"; }
	if($displ{'dwband'} ne "") {  $display.= " ".$text{'pure-users_criteriadwband'}.
	"&nbsp;<input type=text name=d_dwband size=10 value=\"$config{'conf_displaydwband'}\">\n"; }
	if($displ{'upratio'} ne "") {  $display.= " ".$text{'pure-users_criteriaupratio'}.
	"&nbsp;<input type=text name=d_upratio size=10 value=\"$config{'conf_displayupratio'}\">\n"; }
	if($displ{'dwratio'} ne "") {  $display.= " ".$text{'pure-users_criteriadwratio'}.
	"&nbsp;<input type=text name=d_dwratio size=10 value=\"$config{'conf_displaydwratio'}\">\n"; }
	if($displ{'mxfile'} ne "") {  $display.= " ".$text{'pure-users_criteriamax_files'}.
	"&nbsp;<input type=text name=d_mxfile size=10 value=\"$config{'conf_displaymxfile'}\">\n"; }
	if($displ{'mxsize'} ne "") {  $display.= " ".$text{'pure-users_criteriamax_size'}.
	"&nbsp;<input type=text name=d_mxsize size=10 value=\"$config{'conf_displaymxsize'}\">\n"; }
	if($displ{'percfile'} ne "") {  $display.= " ".$text{'pure-users_criteriaper_files'}.
	"&nbsp;<input type=text name=d_percfile size=10 value=\"$config{'conf_displaypercfile'}\">\n"; }
	if($displ{'percsize'} ne "") {  $display.= " ".$text{'pure-users_criteriaper_size'}.
	"&nbsp;<input type=text name=d_percsize size=10 value=\"$config{'conf_displaypercsize'}\">\n"; }
	if($displ{'session'} ne "") {  $display.= " ".$text{'pure-users_criteriamax_sessions'}.
	"&nbsp;<input type=text name=d_sess size=10 value=\"$config{'conf_displaysession'}\">\n"; }

	if ($displ{'chroot'} ne "") {  
	$display.= " <br><br>".$text{'pure-users_criteriachroot'}.
	"&nbsp;<input type=radio name=d_chroot value=0";
	$display.= " checked" if($config{'conf_displaychroot'} == "0");
	$display.= ">$text{'No'} &nbsp;<input type=radio name=d_chroot value=1";
	$display.= " checked" if($config{'conf_displaychroot'} == "1");
	$display.= ">$text{'Yes'}\n";
	$display.= "&nbsp;<input type=radio name=d_chroot value=2";
	$display.= " checked" if($config{'conf_displaychroot'} == "2");
	$display.= ">$text{'Whatever'}\n";
	} if ($config{'conf_displaychroot'} == "2" ) { $config{'conf_displaychroot'} = ""; }

	# Return value if display's preferences are set
	if ( $display ) { return 1; } else { return 0; }


}




if ($in{'action'} eq $text{'delete'}) {
	# Delete one user
	$action="$config{'conf_pureftpdpw'} userdel \"$in{'login'}\" -m";
	open (FIC, "$action |");
    @results=<FIC>; close(FIC);
    if(!$results[0]) 
    { printf "<center><h1>$text{'pure-users_deleteOK'}</h1></center>\n\n",
    $in{'login'}; } else { printf "<center><h1>$text{'pure-users_notdelete'}
    <br>$results[0]</h1></center>\n\n",$in{'login'}; } }


elsif ($in{'action'} eq $text{'pure-users_quotasupdate'}) {
	
	# Check if pure-quotacheck is installed.
	if (!-x $config{'conf_purequotas'}) {
	print "<p><hr><center><h2>",&text('pure-users_quotasconf',
                "<tt>$config{'conf_purequotas'}</tt>",
                "/config.cgi?$module_name"),
          "</h2></center><p>\n<hr>\n";
    } else {

	# Update quotas from home directory
	$action="$config{'conf_purequotas'} -u $in{'uid'} -d \"$in{'home'}\" -g $in{'gid'}";
	open (FIC, "$action |");
    @results=<FIC>; close(FIC);
    if(!$results[0]) 
    { printf "<center><h1>$text{'pure-users_quotasOK'}</h1></center>\n\n",
    $in{'login'}; } else { printf "<center><h1>$text{'pure-users_notquotas'}
    <br>$results[0]</h1></center>\n\n",$in{'login'}; } } }


elsif ($in{'action'} eq $text{'save'}) {
	
	# Modify one user
	$action ="$config{'conf_pureftpdpw'} usermod \"$in{'login'}\" ";
	&Pureparse(); $action.="-m";
	open (FIC, "$action |");
    @results=<FIC>; close(FIC); 

    # Changing user results
    if(!$results[0]) { printf "<center><h1>$text{'pure-users_modifyOK'}
    </h1></center>\n\n",$in{'login'}; } else { printf "<center><h1>
    $text{'pure-users_notmodify'}<br>$results[0]</h1></center>\n\n",
    $in{'login'}; }

    # Change user's password
	if(!$in{'change'} && $in{'action'} eq $text{'save'}) { 
	$action ="(echo \"$in{'passwd2'}\"; echo \"$in{'passwd2'}\") ";
	$action.="| $config{'conf_pureftpdpw'} passwd \"$in{'login'}\" -m";
	open (FIC, "$action |");
    @results=<FIC>; close(FIC);

    # Changing password results
    if($results[0]) 
    { printf "<center><h1>$text{'pure-users_passwdOK'}</h1>
    </center>\n\n",$in{'login'}; } else { printf "<h1><center>
    $text{'pure-users_notpasswd'}</h1></center>\n\n",$in{'login'}; }}
}


elsif ($in{'action'} eq $text{'add'}) {

	$error=""; # Check if all the basic info for new user are present
	   if(!$in{'login'})	{ $error=$text{'pure-users_loginmissing'}; }
	elsif(!$in{'home'})		{ $error=$text{'pure-users_homemissing'}; }
	elsif(!$in{'uid'})		{ $error=$text{'pure-users_uidmissing'}; }
	elsif(!$in{'gid'})		{ $error=$text{'pure-users_gidmissing'}; }
	elsif(!$in{'passwd'})	{ $error=$text{'pure-users_passwdmissing'}; }

	else { # Everything is ok, Add user
	$action ="(echo \"$in{'passwd'}\"; echo \"$in{'passwd'}\") ";
	$action.="| $config{'conf_pureftpdpw'} useradd \"$in{'login'}\" ";
	&Newuser();
	$action.="-m";
	open (FIC, "$action|");
    @results=<FIC>; close(FIC); }
    
    # Adding results
    if($results[0] && !$error) 
    { printf "<center><h1>$text{'pure-users_addOK'}</h1></center>\n\n",
    $in{'login'}; } else { printf "<center><h1>$text{'pure-users_notadd'}
    <br>$error</h1></center>\n\n",$in{'login'}; }
}

print "<center>".&text('pure-users_displaywarning',"#display")."</center><br><br>" if &Setdisplay();


$sure = $text{'pure-users_areyousure'}; 
print "\n\n<hr>\n<center><table border width=60%>\n\n";
print "<tr $tb> <td><b>$text{'pure-users_header'}</b></td></tr>\n";
print "<tr $cb> <td><table>\n\n";

	# Are new users Chroot or not ?
	if($config{'conf_newchroot'}) { $new2=" checked";
	$new1=""; } else{ $new1=" checked"; $new2=""; }
	
# New user form
print <<EOF;

<tr><td valign=top>\
<form action=pure-users.cgi method=POST>
<h2><b>$text{'pure-users_NEWUSER'}</b></h2>
<a href="/config.cgi?pureftpd">$text{'pure-users_defaultsettings'}</a>
</td><td><table border width=100%>
<tr $tb><td colspan=2 align=center><b>$text{'pure-users_NEWUSER'}</b>
</td></tr>
<tr><td><table>
<tr><td nowrap><b>$text{'login'}</b></td><td>
<input name=login size=40 value="$config{'conf_newlogin'}"></td></tr>
<tr><td nowrap><b>$text{'gecos'}</b></td><td>
<input name=gecos size=40 value="$config{'conf_newgecos'}"></td></tr>
<tr><td nowrap><b>$text{'home'}</b></td><td>
<input name=home size=35 value="$config{'conf_newpath'}"> 
<input type=button onClick='ifield=document.forms[0].home; chooser=window.open("/chooser.cgi?type=1&chroot=/&file="+ifield.value,"chooser","toolbar=no,menubar=no,scrollbar=no,width=400,height=300"); chooser.ifield=ifield; window.ifield=ifield;' value="...
">
</td></tr>
<tr><td nowrap><b>$text{'upload_band'}</b></td><td>
<input name=upload_band size=10 value='$config{'conf_newupload'}'> $text{'speed'}</td></tr>
<tr><td nowrap><b>$text{'download_band'}</b></td><td>
<input name=download_band size=10 value='$config{'conf_newdownload'}'> $text{'speed'}</td></tr>
<tr><td nowrap><b>$text{'upload_ratio'}</b></td><td>
<input name=upload_ratio size=10 value='$config{'conf_ratioupload'}'> $text{'Mb'}</td></tr>
<tr><td nowrap><b>$text{'download_ratio'}</b></td><td>
<input name=download_ratio size=10 value='$config{'conf_ratiodownload'}'> $text{'Mb'}</td></tr>
<tr><td nowrap><b>$text{'max_files'}</b></td><td>
<input name=max_files size=10 value='$config{'conf_newmaxfiles'}'> $text{'items'}</td></tr>
<tr><td nowrap><b>$text{'max_size'}</b></td><td>
<input name=max_size size=10 value='$config{'conf_newmaxsize'}'> $text{'Mb'}</td></tr>
<tr><td nowrap><b>$text{'allow_local_IP'} </b></td><td>
<input name=allow_local_IP size=40 value='$config{'conf_newallowlocal'}'></td></tr>
<tr><td nowrap><b>$text{'deny_local_IP'} </b></td><td>
<input name=deny_local_IP size=40 value='$config{'conf_newdenylocal'}'></td></tr>
<tr><td nowrap><b>$text{'allow_client_IP'} </b></td><td>
<input name=allow_client_IP size=40 value='$config{'conf_newallowclient'}'></td></tr>
<tr><td nowrap><b>$text{'deny_client_IP'} </b></td><td>
<input name=deny_client_IP size=40 value='$config{'conf_newdenyclient'}'></td></tr>
<tr><td nowrap><b>$text{'time'} </b></td><td>
<input name=time size=10 value='$config{'conf_newtime'}'> hhmm-hhmm</td></tr>
<tr><td nowrap><b>$text{'max_sessions'} </b></td><td>
<input name=max_sessions size=10 value='$config{'conf_maxsession'}'></td></tr>
<tr><td nowrap><b>$text{'chroot'} </b></td><td>
<input type=radio name=chroot value="-d"$new1> $text{'Yes'} 
<input type=radio name=chroot value="-D"$new2> $text{'No'}</td></tr>
<tr><td nowrap><b>$text{'passwd'} </b></td><td>
<input size=30 name=passwd value=''></td></tr>
<tr><td><input type=submit class=submit name=action value="$text{'add'}">
</td><td><b>$text{'uid'}</b> 
<input name=uid size=10 value='$config{'conf_newuid'}'>
<input type=button onClick='ifield=document.forms[0].uid;chooser=window.open("/user_chooser.cgi?multi=0&user="+escape(ifield.value),"chooser","toolbar=no,menubar=no,scrollbars=yes,width=300,height=200"); chooser.ifield=ifield;window.ifield=ifield' value="
...">
<b>$text{'gid'}</b> 
<input name=gid size=10 value='$config{'conf_newgid'}'> 
<input type=button onClick='ifield=document.forms[0].gid;chooser=window.open("/group_chooser.cgi?multi=0&group="+escape(ifield.value),"chooser","toolbar=no,menubar=no,scrollbars=yes,width=300,height=200"); chooser.ifield=ifield;window.ifield=ifield;' valu
e="...">
</td></tr></table>
</center></td></tr></table></form><br></td></tr>

EOF

$lines = &read_file_lines("$config{'conf_pureftpdldap'}"); 
$j=0;$k=0; $percent_size=""; $percent_file=""; 


# Loop to parse each user from the pureftpd.passwd
foreach $i ( sort sort_as_wanted(@$lines) ) {

	# parse the user's line and split each values
	local ($login, $passwd, $uid, $gid, $gecos, $home,
	$upload_band, $download_band, $upload_ratio, $download_ratio,
	$max_sessions, $max_files, $max_size, 
	$allow_local_IP, $deny_local_IP, 
	$allow_client_IP, $deny_client_IP, $time) = split(/:/, $i);

	# Check if the user is chrooted
	if ($home =~ /^(.*)\.\/$/) { $home = $1; 
	$chroot = 1; } else { $chroot = 0; }
	
	# compute the proper value of Mb and bandwith
	if($max_size){ $max_size = ($max_size/1048576); }
	if($upload_band){ $upload_band = int($upload_band/1024); }
	if($download_band){ $download_band = int($download_band/1024); }
	
	# Check quotas if "max_size" or "max_files" are set
	if($max_files || $max_size ) { $quotas="<br><br>\n";
	if(-e "$home/.ftpquota") { 
	$files = &read_file_lines("$home/.ftpquota");
	$files = $file_cache{"$home/.ftpquota"}[0];
	($file_quotas,$size_quotas) = split(/ /, $files);
	$size_quotas=int($size_quotas/1048576);
	if($max_files){ # if max_files set then compute
	$percent_size=int(($file_quotas/$max_files)*100);
	$quotas.=" $text{'file_quotas'}: <b>". $percent_size .
	"%</b> ($file_quotas ".$text{'items'}.")";}
	if($max_size){ # if max_size set then compute
	$percent_file=int(($size_quotas/$max_size)*100);
	$quotas.=" $text{'size_quotas'}: <b>". $percent_file .
	"%</b> ($size_quotas ".$text{'Mb'}.")";}
	} else { $quotas.=$text{'pure-users_quotasnone'}; 
	$percent_size=""; $percent_file=""; }
	$quotas.="<br>\n<input type=submit class=submit ".
	"name=action value=\"$text{'pure-users_quotasupdate'}\">\n";
	if(($max_files && $max_files<=$file_quotas) 
	|| ($max_size && $max_size<=$size_quotas))
			{ $exceeded="<b>$text{'pure-users_quotaexceeded'}</b>"; }
			else { $exceeded=""; }
	} else { $quotas=""; $exceeded=""; $percent_size=""; $percent_file=""; } 



	if ( # Test if the current user matches the display configuration preferences
	   ($config{'conf_displaylogin'} eq "" || $login =~ /$config{'conf_displaylogin'}/)
	&& ($config{'conf_displaygecos'} eq "" || $gecos =~ /$config{'conf_displaygecos'}/)
	&& ($config{'conf_displayhome'}  eq "" || $home =~ /$config{'conf_displayhome'}/)
	&& ($config{'conf_displaychroot'} eq "" || $chroot eq $config{'conf_displaychroot'})
	&& ($minuid eq "" || $uid >= $minuid) && ($maxuid eq "" || $uid <= $maxuid)
	&& ($mingid eq "" || $gid >= $mingid) && ($maxgid eq "" || $gid <= $maxgid)
	&& ($minupb eq "" || $upload_band >= $mingid) && ($maxupb eq "" || $upload_band <= $maxupb)
	&& ($mindlb eq "" || $download_band >= $mindlb) && ($maxdlb eq "" || $download_band <= $maxdlb)
	&& ($minupr eq "" || $upload_ratio >= $minupr) && ($maxupr eq "" || $upload_ratio <= $maxupr)
	&& ($mindlr eq "" || $download_ratio >= $mindlr) && ($maxdlr eq "" || $download_ratio <= $maxdlr)
	&& ($minfil eq "" || $max_files >= $minfil) && ($maxfil eq "" || $max_files <= $maxfil)
	&& ($minsiz eq "" || $max_size >= $minsiz) && ($maxsiz eq "" || $max_size <= $maxsiz)
	&& ($minprf eq "" || $percent_size >= $minprf) && ($maxprf eq "" || $percent_size <= $maxprf)
	&& ($minprs eq "" || $percent_file >= $minprs) && ($maxprs eq "" || $percent_file <= $maxprs)
	&& ($minses eq "" || $max_sessions >= $minses) && ($maxses eq "" || $max_sessions <= $maxses)
	) { $j++; } else { $k++; next; }


	# Display the current user's form
	print "<tr><td valign=top>\n";
	print "<form action=pure-users.cgi method=POST>\n";
	print "<input type=hidden name=login value=\"$login\">\n";
	print "<h2><b>$login</b></h2>\n";
	print "<input type=submit class=submit name=action value=\"$text{'save'}\">\n";
	print "<input type=submit class=submit name=action value=\"$text{'delete'}\" ";
	print "onClick=\"if (window.confirm('$sure $login ?')) { return true; } else { return false; }\">";
	print "<br><br><font color=red>$exceeded</font></td><td><table border width=100%>\n";     
	print "<tr $tb><td colspan=2 align=center><b>$login</b></td></tr>",
	print "<tr><td><table>\n";
	print "<tr><td nowrap><b>$text{'gecos'}</b></td><td>",
	"<input name=gecos size=40 value=\"$gecos\"></td></tr>\n";
	print "<tr><td nowrap><b>$text{'home'}</b></td><td>",
	"<input name=home size=35 value=\"$home\">",
	"<input type=button onClick='ifield=document.forms[$j].home; chooser=window.open(\"/chooser.cgi?",
	"type=1&chroot=/&file=\"+ifield.value,\"chooser\",\"toolbar=no,menubar=no,scrollbar=no,width=400,",
	"height=300\"); chooser.ifield=ifield; window.ifield=ifield;' value=\"...\">";

	print "</td></tr>\n<tr><td nowrap><b>$text{'upload_band'}</b></td><td>",
	"<input name=upload_band size=10 value=\"$upload_band\"> $text{'speed'}</td></tr>\n";
	print "<tr><td nowrap><b>$text{'download_band'}</b></td><td>",
	"<input name=download_band size=10 value=\"$download_band\"> $text{'speed'}</td></tr>\n";
	print "</td></tr>\n<tr><td nowrap><b>$text{'upload_ratio'}</b></td><td>",
	"<input name=upload_ratio size=10 value=\"$upload_ratio\"> $text{'Mb'}</td></tr>\n";
	print "<tr><td nowrap><b>$text{'download_ratio'}</b></td><td>",
	"<input name=download_ratio size=10 value=\"$download_ratio\"> $text{'Mb'}</td></tr>\n";

	print "<tr><td nowrap><b>$text{'max_files'}</b></td><td>",
	"<input name=max_files size=10 value=\"$max_files\"> $text{'items'}</td></tr>\n";
	print "<tr><td nowrap><b>$text{'max_size'}</b></td><td>",
	"<input name=max_size size=10 value=\"$max_size\"> $text{'Mb'}</td></tr>\n";

	print "<tr><td nowrap><b>$text{'allow_local_IP'}</b></td><td>",
	"<input name=allow_local_IP size=40 value=\"$allow_local_IP\"></td></tr>\n";
	print "<tr><td nowrap><b>$text{'deny_local_IP'}</b></td><td>",
	"<input name=deny_local_IP size=40 value=\"$deny_local_IP\"></td></tr>\n";

	print "<tr><td nowrap><b>$text{'allow_client_IP'}</b></td><td>",
	"<input name=allow_client_IP size=40 value=\"$allow_client_IP\"></td></tr>\n";
	print "<tr><td nowrap><b>$text{'deny_client_IP'}</b></td><td>",
	"<input name=deny_client_IP size=40 value=\"$deny_client_IP\"></td></tr>\n";

	print "<tr><td nowrap><b>$text{'time'}</b></td><td>",
	"<input name=time size=10 value=\"$time\"> hhmm-hhmm</td></tr>\n";
	print "<tr><td nowrap><b>$text{'max_sessions'}</b></td><td>",
	"<input name=max_sessions size=10 value=\"$max_sessions\"></td></tr>\n";

	print "<tr><td nowrap><b>$text{'chroot'}</b></td><td>",
	"<input type=radio name=chroot value=\"-d\"",
	$chroot ? " checked> $text{'Yes'} " : "> $text{'Yes'} ",
	"<input type=radio name=chroot value=\"-D\"",
	$chroot ? "> $text{'No'}</td></tr>" : " checked> $text{'No'}</td></tr>";

	print " </table><center><b>$text{'uid'}</b> <input name=uid size=10 value='$uid'>\n";
	print " <input type=button onClick='ifield=document.forms[$j].uid;chooser=window.open",
	"(\"/user_chooser.cgi?multi=0&user=\"+escape(ifield.value),\"chooser\",\"toolbar=no,",
	"menubar=no,scrollbars=yes,width=300,height=200\"); chooser.ifield=ifield;window.ifield=ifield' value=\"...\"> \n";
	print " <b>$text{'gid'}</b> <input name=gid size=10 value='$gid'> \n";
	print " <input type=button onClick='ifield=document.forms[$j].gid;chooser=window.open",
	"(\"/group_chooser.cgi?multi=0&group=\"+escape(ifield.value),\"chooser\",\"toolbar=no,",
	"menubar=no,scrollbars=yes,width=300,height=200\"); chooser.ifield=ifield;window.ifield=ifield;' value=\"...\"> \n";
	print "	<br><b>$text{'passwd'}</b> <input type=radio name=change value=1 checked>&nbsp;";
	print "$text{'change'} | <input type=radio name=change value=0>";
	print "<input name=passwd2 size=30 value=''>\n";
	print " $quotas\n";
	print "</center></td></tr></table></form></td></tr>\n\n\n";
}


# Now display the "Display form"      
print "<tr><td colspan=2><a name='display'></a><br><br><center>";
print &text('pure-users_displayresult',$j,$k)."<br>";
print "<br><font color=red>$text{'pure-users_displaynone'}</font>" if ($j==0 && $k>0) ;
print "<form action=pure-users.cgi method=GET>\n";
print "$text{'pure-users_display'}<br>";
print "<input type=radio name=sort value=login";
print " checked" if($sort eq "login" || $sort eq "");
print "> $text{'pure-users_criterialogin'} \n";
print "<input type=radio name=sort value=gecos";
print " checked" if($sort eq "gecos");
print "> $text{'pure-users_criteriagecos'} \n";
print "<input type=radio name=sort value=home";
print " checked" if($sort eq "home");
print "> $text{'pure-users_criteriahome'} \n";
print "<input type=radio name=sort value=uid";
print " checked" if($sort eq "uid");
print "> $text{'pure-users_criteriauid'} \n";
print "<input type=radio name=sort value=gid";
print " checked" if($sort eq "gid");
print "> $text{'pure-users_criteriauid'}<br><br>\n";
print "<input type=submit value=\"$text{'pure-users_displayagain'}\">";
print "$display</form>";
		
		
		

print	"</center></td></tr></table>\n\n</td></tr></table></center>\n\n";

&footer("", $text{'index_return'});
