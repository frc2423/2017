"use strict";

$('[name=climb]').on('click',function() {
	if ($(this).is(".climb")) {
		$(this).addClass(climbing);
		$(this).removeClass(climb);
	} else {
		$(this).addClass(climb);
		$(this).removeClass(climbing);
	}
	
});