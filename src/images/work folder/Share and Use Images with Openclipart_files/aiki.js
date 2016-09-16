/*
 * Aiki framework
 *
 * @author		Aikilab http://www.aikilab.com
 * @copyright  (c) 2008-2010 Aikilab
 * @license		http://www.fsf.org/licensing/licenses/agpl-3.0.html
 * @link		http://www.aikiframework.org
 */

var stop = 0;

function  globalajaxify(file, targetwidget){

if (stop != 1){
	stop = 1;
	$('<div id="loading_box"><span>Loading please wait...</span></div>').hide().appendTo(targetwidget).fadeIn(1000);
	$.get(file,function(data) {
		$('#loading_box').fadeOut(500, function() { $(this).remove(); 
		$(targetwidget).hide().fadeIn(500).html(data);
		$('#edit_form').ajaxForm(function() { $("#edit_form").html("Edited successfully"); });
		});
		stop = 0;
	});
}
}

$(document).ready(function(){

// wolf 20140530 - live is deprected after jquery 1.7, see
//                 http://api.jquery.com/live/
//	$('a').live('click', function() {
	$( document ).on("click", "a", function() {
		if($(this).attr('rel') && $(this).attr('href') && $(this).attr('rev')) {
			globalajaxify($(this).attr('href')+'?noheaders=true&noheaders=true&widget='+$(this).attr('rel'), $(this).attr('rev'));
			return false;
		}
	});
//	$('span').live('click', function() {
	$( document ).on("click", "span", function() {
		if($(this).attr('rel') && $(this).attr('rev')) {
			globalajaxify('?noheaders=true&noheaders=true&widget='+$(this).attr('rel'), $(this).attr('rev'));
			return false;
		}
	});
});
