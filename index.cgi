#!/usr/bin/perl
# Display the Pure-FTPd main menu.

do '../web-lib.pl';
&init_config(); &ReadParse();
use Socket;
$| = 1;

&header($text{'index_title'}, undef, "intro", 1, 1, undef, $text{'index_mail'});
print "<hr>\n";

# Check if there is CSS styles
if ($config{'conf_pureCSS'}) { print "<STYLE type=\"text/css\">
$config{'conf_pureCSS'}\n</STYLE>\n\n"; }

# Check if ftpd is installed.
if (!-x $config{'ftpd_path'}) {
    print "<p>", 
          &text('index_eftpd', 
		"<tt>$config{'ftpd_path'}</tt>",
		"/config.cgi?$module_name"), 
          "<p>\n";
    print "<hr>\n";
    &footer("/", $text{'index'});
    exit;
}

# Display table of icons.
@names = ('pure-options', 'pure-conf', 'pure-users', 'pure-monitor');
@links = map { "${_}.cgi" } @names;
@titles = map { $text{"${_}_title"} } @names;
$links[0]="/config.cgi?pureftpd";
if($config{'conf_pureicons'}){
@icons = map { "images/${_}48.gif" } @names;
&icons_table(\@links, \@titles, \@icons, 4, '', 48, 48);
} else { @icons = map { "images/${_}128.gif" } @names;
&pure_icons_table(\@links, \@titles, \@icons, 4, '', 128, 128); }
print "<hr>\n";


&footer("/", $text{'index'});



# icons_table(&links, &titles, &icons, [columns], [href], [width], [height])
# Renders a 4-column table of icons !!!!! WITHOUT BORDER !!!!!
sub pure_icons_table
{
local ($i, $need_tr);
local $cols = $_[3] ? $_[3] : 4;
local $per = int(100.0 / $cols);
local $w = !defined($_[4]) ? "width=48" : $_[4] ? "width=$_[4]" : "";
local $h = !defined($_[5]) ? "height=48" : $_[5] ? "height=$_[5]" : "";
print "<table width=100% cellpadding=5>\n";
for($i=0; $i<@{$_[0]}; $i++) {
	if ($i%$cols == 0) { print "<tr>\n"; }
	print "<td width=$per% align=center valign=top>\n";
	print "<a href=\"".$_[0]->[$i]."\" $_[4]><img src=\"".$_[2]->[$i]."\" ",
	      "alt=\"\" border=0 $w $h></a><br>\n";
	print "<a href=\"".$_[0]->[$i]."\">".$_[1]->[$i]."</a>\n";
	print "</td>\n";
        if ($i%$cols == $cols-1) { print "</tr>\n"; }
        }
while($i++%$cols) { print "<td width=$per%></td>\n"; $need_tr++; }
print "</tr>\n" if ($need_tr);
print "</table><p>\n";
}
