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
	$(this).addClass('pressed');
	var $el = $(this);
	setTimeout(function() {
		$el.removeClass('pressed');
	}, 500);
})

$('[name=roper]').on('click', function() {
	$(this).addClass('pressed');
	var $el = $(this);
	setTimeout(function() {
		$el.removeClass('pressed');
	}, 500);
})

$('[name=ropet]').on('click', function() {
	$(this).addClass('pressed');
	var $el = $(this);
	setTimeout(function() {
		$el.removeClass('pressed');
	}, 500);
})

$('[name=ropeb]').on('click', function() {
	$(this).addClass('pressed');
	var $el = $(this);
	setTimeout(function() {
		$el.removeClass('pressed');
	}, 500);
})

