"use strict";

$('[name=climb]').on('click', function() {
	NetworkTables.putValue("/SmartDashboard/climberspeed", 1);
	if ($(this).hasClass('climb')) {
		$(this).addClass('climbing');
		$(this).removeClass('climb');
	} else {
		NetworkTables.putValue("/SmartDashboard/climberspeed", 0);
		$(this).addClass('climb');
		$(this).removeClass('climbing');
	}
});

$('[name=ropel]').on('click', function() {
	NetworkTables.putValue("/SmartDashboard/align", 1)
	$(this).addClass('pressed');
	$('.airship_aligning').css('display', 'block')
	var $el = $(this);
	setTimeout(function() {
		$el.removeClass('pressed');
		NetworkTables.putValue("/SmartDashboard/align", 0);
		$('.airship_aligning').css('display', 'none')
	}, 3000);
})

$('[name=roper]').on('click', function() {
	NetworkTables.putValue("/SmartDashboard/align", 2)
	$(this).addClass('pressed');
	$('.airship_aligning').css('display', 'block')
	var $el = $(this);
	setTimeout(function() {
		$el.removeClass('pressed');
		NetworkTables.putValue("/SmartDashboard/align", 0);
		$('.airship_aligning').css('display', 'none')
	}, 3000);
})

$('[name=ropet]').on('click', function() {
	NetworkTables.putValue("/SmartDashboard/align", 3)
	$(this).addClass('pressed');
	$('.airship_aligning').css('display', 'block')
	var $el = $(this);
	setTimeout(function() {
		$el.removeClass('pressed');
		NetworkTables.putValue("/SmartDashboard/align", 0);
		$('.airship_aligning').css('display', 'none')
	}, 3000);
})

$('[name=ropeb]').on('click', function() {
	NetworkTables.putValue("/SmartDashboard/align", 4)
	$(this).addClass('pressed');
	$('.airship_aligning').css('display', 'block')
	var $el = $(this);
	setTimeout(function() {
		$el.removeClass('pressed');
		NetworkTables.putValue("/SmartDashboard/align", 0);
		$('.airship_aligning').css('display', 'none')
	}, 3000);
})


NetworkTables.addKeyListener("/SmartDashboard/angle", function(key, value, isNew){
	if (value == 500) {	
		$('#angle').text("?");
	} else {
		$('#angle').text(value);
	}
}, true);

NetworkTables.addKeyListener("/SmartDashboard/switch", function(key, value, isNew){
    // do something with the values as they change
	if (value == 1) {
		$('#auto_chooser').css('display', 'block');
		$('#sensors').css('display', 'none')
	}
	else if (value == 2) {
		$('#auto_chooser').css('display', 'none');
		$('#sensors').css('display', 'block')
	}
}, true);