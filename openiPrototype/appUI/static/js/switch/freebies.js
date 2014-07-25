var stylesChanged = false;
var randomStyle = false;
var onoff = {};
var deviceskins = {}

onoff.init = function(){
	
	onoff.iniGallery();
	
	$('input[type=text]').not('.slider-value').not('.picker').change(function(){
		stylesChanged = true;
		randomStyle = false;
		onoff.renderCss();
		onoff.renderHtml();
	});
	
	$('input.slider-value').change(function(){
		stylesChanged = true;
		randomStyle = false;
		var val = parseInt($(this).val())
		if(isNaN(val)) {
			val = $(this).get(0).defaultValue;
		}
		$(this).prev('.slider').slider('value', val)
		$(this).val(val)
		onoff.renderCss();
		//onoff.renderHtml();
	});


	$('input[name=style]').change(function(){
		onoff.togglePropertyState($(this).val());
		if(!stylesChanged) {
			onoff.resetStyle($(this).val());
		}
		onoff.renderCss();
		onoff.renderHtml();
	});
	
	$('input[name=switch-default-state]').change(function(){
		stylesChanged = true;
		randomStyle = false;
		onoff.renderHtml();
	});
	
	$('.slider').each(function(){
		$(this).slider({
			range: "min",
			value: parseInt($(this).next('.slider-value').val()),
			min: parseInt($(this).attr('data-min')),
			max: parseInt($(this).attr('data-max')),
			slide: function(e, ui){
				$(this).next('.slider-value').val(ui.value);
				onoff.renderCss(false);
			},
			stop: function(e, ui){
				stylesChanged = true;
				randomStyle = false;
				onoff.renderCss(true);
			}
		});
	})
	
	$('.picker').miniColors({
		letterCase: 'uppercase'
	}).bind('blur', function(){
		stylesChanged = true;
		randomStyle = false;
		onoff.renderCss();
	});
	
	$('#revert-style').click(function(){
		stylesChanged = false;
		onoff.resetStyle($('input[name=style]:checked').val());
		onoff.renderCss();
		onoff.renderHtml();
		return false;
	}); 
	
	$('#dual-switch-color').change(function(){
		stylesChanged = true;
		randomStyle = false;
		if($(this).is(':checked')) {
			$('#active-switch-color-property, #inactive-switch-color-property').slideDown();
			$('#switch-color-property, #switch-color-property').slideUp();
			$('#active-bg-color').attr('disabled', 'disabled')
		} else {
			$('#active-switch-color-property, #inactive-switch-color-property').slideUp();
			$('#switch-color-property, #switch-color-property').slideDown();
			$('#active-bg-color').removeAttr('disabled')
		}
		onoff.renderCss();
		onoff.renderHtml();
	})
	
	
	onoff.demoContainerTopY = $('#component-demo-wrapper').get(0).offsetTop; 
	
	$(window).scroll(function(){
		if(window.pageYOffset > onoff.demoContainerTopY) {
			$('#component-demo-wrapper').addClass('fixed');
		} else {
			$('#component-demo-wrapper').removeClass('fixed');
		}
	})
}

onoff.renderCss = function(redrawCode){
	
	if(typeof(redrawCode) == "undefined") { redrawCode = true; }
	
	var width = Number($('#width').val());
	var height = Number($('#height').val());
	var borderRadius = Number($('#border-radius').val());
	var fontSize = Number($('#font-size').val());
	var spacing = Number($('#spacing').val());
	var switchSize = Number($('#switch-size').val());
	var activeBgColor = $('#active-bg-color').val();
	var activeTextColor = $('#active-text-color').val();
	var inactiveBgColor = $('#inactive-bg-color').val();
	var inactiveTextColor = $('#inactive-text-color').val();
	var switchColor = $('#switch-color').val();
	var switchActiveColor = $('#active-switch-color').val();
	var switchInactiveColor = $('#inactive-switch-color').val();
	var borderColor = $('#switch-border-color').val();
	var borderWidth = 2;
	var dualSwitch = $('#dual-switch-color').is(':checked');
	var switchMargin;
	var switchSpacing = 4;
	var lineHeight = height;
	var activeText = $('#active-text').val();
	var inactiveText = $('#inactive-text').val();
	
	var style = $('[name=style]:checked').val()
	switch(style) {
	case 'ios5': 
		borderRadius = height;
		switchSize = height;
		switchMargin = (height - switchSize)/2;
		break;
	case 'ios4': 
		borderRadius = 5;
		//switchSize = height;
		switchMargin = 0;
		break;
	case 'android': 
		borderRadius = 0;
		borderWidth = 0;
		switchMargin = 0;
		activeBgColor = inactiveBgColor;
		break;
	case 'metro': 
		borderRadius = 0;
		borderWidth = 2;
		switchMargin = 0;
		switchSpacing = 0;
		lineHeight = height - 4;
		break;
	default: 
		switchMargin = (height - switchSize)/2;
		break;
	}
	
	if(dualSwitch) {
		activeBgColor = inactiveBgColor;
		switchColor = switchInactiveColor;
	}
	
	$('.onoffswitch2').addClass('transition-off')
	
	var _str = '';
	_str += '.onoffswitch2 {\r\n'
	_str += '    position: relative; width: '+width+'px;\r\n'
	_str += '    -webkit-user-select:none; -moz-user-select:none; -ms-user-select: none;\r\n'
	_str += '}\r\n'
	_str += '\r\n'
	_str += '.onoffswitch2-checkbox {\r\n'
	_str += '    display: none;\r\n'
	_str += '}\r\n'
	_str += '\r\n'
	_str += '.onoffswitch2-label {\r\n'
	_str += '    display: block; overflow: hidden; cursor: pointer;\r\n'
	_str += '    border: '+borderWidth+'px solid '+borderColor+'; border-radius: '+borderRadius+'px;\r\n'
	_str += '}\r\n'
	_str += '\r\n'
	_str += '.onoffswitch2-inner {\r\n'
	_str += '    display: block; width: 200%; margin-left: -100%;\r\n'
	_str += '    -moz-transition: margin 0.3s ease-in 0s; -webkit-transition: margin 0.3s ease-in 0s;\r\n'
	_str += '    -o-transition: margin 0.3s ease-in 0s; transition: margin 0.3s ease-in 0s;\r\n' 
	_str += '}\r\n'
	_str += '\r\n'
	if(style=="android") {
		_str += '.onoffswitch2-inner > span {\r\n'
	} else {
		_str += '.onoffswitch2-inner:before, .onoffswitch2-inner:after {\r\n'
	}
	_str += '    display: block; float: left; '+((style=="android") ? 'position: relative; ' : '') + 'width: 50%; height: '+height+'px; padding: 0; line-height: '+lineHeight+'px;\r\n'
	_str += '    font-size: '+fontSize+'px; color: white; font-family: Trebuchet, Arial, sans-serif; font-weight: bold;\r\n'
	_str += '    -moz-box-sizing: border-box; -webkit-box-sizing: border-box; box-sizing: border-box;\r\n'
	if(style == 'ios5') {
		_str += '    border-radius: '+borderRadius+'px;\r\n'
		_str += '    box-shadow: 0px '+(height/2)+'px 0px rgba(0,0,0,0.08) inset;\r\n'
	}
	if(style=="metro") {
		_str += '    border: 2px solid transparent;\r\n'
		_str += '    background-clip: padding-box;\r\n'
	}
	_str += '}\r\n'
	_str += '\r\n'
	if(style=="android") {
		_str += '.onoffswitch2-inner .onoffswitch2-active {\r\n'
	} else {
		_str += '.onoffswitch2-inner:before {\r\n'
		_str += '    content: "'+activeText+'";\r\n'
	}
	_str += '    padding-left: '+spacing+'px;\r\n'
	_str += '    background-color: '+activeBgColor+'; color: '+activeTextColor+';\r\n'
	if(style == 'ios5') {
		_str += '    border-radius: '+borderRadius+'px 0 0 '+borderRadius+'px;\r\n'
	}
	_str += '}\r\n'
	_str += '\r\n'
	if(style=="android") {
		_str += '.onoffswitch2-inner .onoffswitch2-inactive {\r\n'
	} else {
		_str += '.onoffswitch2-inner:after {\r\n'
		_str += '    content: "'+inactiveText+'";\r\n'
	}
	_str += '    padding-right: '+spacing+'px;\r\n'
	_str += '    background-color: '+inactiveBgColor+'; color: '+inactiveTextColor+';\r\n'
	_str += '    text-align: right;\r\n'
	if(style == 'ios5') {
		_str += '    border-radius: 0 '+borderRadius+'px '+borderRadius+'px 0;\r\n'
	}
	_str += '}\r\n'
	_str += '\r\n'
	if(style=="android") {
		_str += '.onoffswitch2-switch {\r\n'
		_str += '    display: block; width: '+switchSize+'px; margin: '+switchMargin+'px; text-align: center; \r\n'
		_str += '    border: '+borderWidth+'px solid '+borderColor+';border-radius: '+borderRadius+'px; \r\n'
		_str += '    position: absolute; top: 0; bottom: 0;\r\n'
		_str += '}\r\n'
		_str += '.onoffswitch2-active .onoffswitch2-switch {\r\n'
		_str += '    background: '+switchActiveColor+'; left: 0;\r\n'
		_str += '}\r\n'
		_str += '.onoffswitch2-inactive .onoffswitch2-switch {\r\n'
		_str += '    background: '+switchInactiveColor+'; right: 0;\r\n'
		_str += '}\r\n'
		_str += '\r\n'
		_str += '.onoffswitch2-active .onoffswitch2-switch:before {\r\n'
		_str += '    content: " "; position: absolute; top: 0; left: '+switchSize+'px; \r\n'
		_str += '    border-style: solid; border-color: '+switchActiveColor+' transparent transparent '+switchActiveColor+'; border-width: '+parseInt(height/2)+'px '+parseInt(width*0.1)+'px;\r\n'
		_str += '}\r\n'
		_str += '\r\n'
		_str += '\r\n'
		_str += '.onoffswitch2-inactive .onoffswitch2-switch:before {\r\n'
		_str += '    content: " "; position: absolute; top: 0; right: '+switchSize+'px; \r\n'
		_str += '    border-style: solid; border-color: transparent '+switchInactiveColor+' '+switchInactiveColor+' transparent; border-width: '+parseInt(height/2)+'px '+parseInt(width*0.1)+'px;\r\n'
		_str += '}\r\n'
		_str += '\r\n'
	} else {
		_str += '.onoffswitch2-switch {\r\n'
		_str += '    display: block; width: '+switchSize+'px; margin: '+switchMargin+'px;\r\n'
		_str += '    background: '+switchColor+';\r\n'
		if(style!="metro") {
			_str += '    border: '+borderWidth+'px solid '+borderColor+'; border-radius: '+borderRadius+'px;\r\n'
		}
		_str += '    position: absolute; top: 0; bottom: 0; right: '+(width-(switchSize + switchMargin*2 + switchSpacing))+'px;\r\n'
		_str += '    -moz-transition: all 0.3s ease-in 0s; -webkit-transition: all 0.3s ease-in 0s;\r\n';
		_str += '    -o-transition: all 0.3s ease-in 0s; transition: all 0.3s ease-in 0s; \r\n'
		if(style == 'ios4') {
			_str += '    background-image: -moz-linear-gradient(center top, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0) 100%);\r\n';
			_str += '    background-image: -webkit-linear-gradient(center top, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0) 100%);\r\n';
			_str += '    background-image: -o-linear-gradient(center top, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0) 100%);\r\n';
			_str += '    background-image: linear-gradient(center top, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0) 100%);\r\n'
		}
		if(style == 'ios5') {
			_str += '    background-image: -moz-linear-gradient(center top, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0) 80%); \r\n';
			_str += '    background-image: -webkit-linear-gradient(center top, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0) 80%); \r\n';
			_str += '    background-image: -o-linear-gradient(center top, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0) 80%); \r\n';
			_str += '    background-image: linear-gradient(center top, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0) 80%);\r\n'
			_str += '    box-shadow: 0 1px 1px white inset;\r\n'
		}
		_str += '}\r\n'
	}
	_str += '\r\n'
	_str += '.onoffswitch2-checkbox:checked + .onoffswitch2-label .onoffswitch2-inner {\r\n'
	_str += '    margin-left: 0;\r\n'
	_str += '}\r\n'
	_str += '\r\n'
	if(style!="android") {
		_str += '.onoffswitch2-checkbox:checked + .onoffswitch2-label .onoffswitch2-switch {\r\n'
		_str += '    right: 0px; \r\n'
		if(dualSwitch) {
			_str += '    background-color: '+switchActiveColor+'; \r\n'
		}
		_str += '}\r\n'
	}
	
	$('#css').html('<pre>'+_str+'</pre>')
	$('#onoffswitch2-style').html(_str)
	
	if(redrawCode) {
		$(".code.code-css > pre").snippet("css", {
			style: "proto",
			showNum: false,
			menu: false,
			clipboard: '/freebies/resources/ZeroClipboard.swf'
		});
	}
	
	$('#component-demo-container').css({
		marginTop: '-' + parseInt(height/2) + 'px',
		marginLeft: '-' + parseInt(width/2) + 'px'
	})
	
	$('.onoffswitch2').removeClass('transition-off')
}

onoff.renderHtml = function() {
	var style = $('input[name=style]:checked').val();
	var activeText = $('#active-text').val();
	var inactiveText = $('#inactive-text').val();
	var state = $('#switch-default-state').is(':checked') ? ' checked' : '';
	var dualSwitch = $('#dual-switch-color').is(':checked');
	$('#component-demo-container .onoffswitch2-switch, #component-demo-container .onoffswitch2-active, #component-demo-container .onoffswitch2-inactive').remove();
	//$('#component-demo-container').find('.onoffswitch2-active').text('').end().find('.onoffswitch2-inactive').text('');
	
	var _str = '';
	if(style=="android") {
		_str += '<div class="onoffswitch2">\r\n'
		_str += '    <input type="checkbox" name="onoffswitch2" class="onoffswitch2-checkbox" id="myonoffswitch2"'+state+'>\r\n'
		_str += '    <label class="onoffswitch2-label" for="myonoffswitch2">\r\n'
		_str += '        <span class="onoffswitch2-inner">\r\n'
		_str += '            <span class="onoffswitch2-active"><span class="onoffswitch2-switch">'+activeText+'</span></span>\r\n'
		_str += '            <span class="onoffswitch2-inactive"><span class="onoffswitch2-switch">'+inactiveText+'</span></span>\r\n'
		_str += '        </span>\r\n'
		_str += '    </label>\r\n'
		_str += '</div>\r\n'
		$('#component-demo-container .onoffswitch2-inner').prepend('<span class="onoffswitch2-active"><span class="onoffswitch2-switch">'+activeText+'</span></span><span class="onoffswitch2-inactive"><span class="onoffswitch2-switch">'+inactiveText+'</span></span>')
	} else {
		_str += '<div class="onoffswitch2">\r\n'
		_str += '    <input type="checkbox" name="onoffswitch2" class="onoffswitch2-checkbox" id="myonoffswitch2"'+state+'>\r\n'
		_str += '    <label class="onoffswitch2-label" for="myonoffswitch2">\r\n'
		_str += '        <span class="onoffswitch2-inner"></span>\r\n'
		//_str += '            <div class="onoffswitch2-active">'+activeText+'</div>\r\n'
		//_str += '            <div class="onoffswitch2-inactive">'+inactiveText+'</div>\r\n'
		//_str += '        </div>\r\n'
		_str += '        <span class="onoffswitch2-switch"></span>\r\n'
		_str += '    </label>\r\n'
		_str += '</div>\r\n'
		$('#component-demo-container .onoffswitch2-label').append('<span class="onoffswitch2-switch"></span>')
	}
	
	$('<pre/>').text(_str).appendTo($('#html').empty());
	
	$(".code.code-html > pre").snippet("html", {
		style: "proto",
		showNum: false,
		menu: false,
		clipboard: '/freebies/resources/ZeroClipboard.swf'
	});
	
}

onoff.togglePropertyState = function(style){
	switch (style) {
	case 'ios4':
		$('#border-radius').attr('disabled', 'disabled');
		$('#border-radius-slider').slider('disable');
		$('#switch-size, #switch-color, #switch-border-color, #active-bg-color').removeAttr('disabled');
		$('#switch-size-slider').slider('enable');
		$('#active-switch-color-property, #inactive-switch-color-property').hide();
		$('#switch-color-property').show();
		$('#dual-switch-color').removeAttr('checked').attr('disabled', 'disabled')
		break;
	case 'ios5':
		$('#border-radius, #switch-size').attr('disabled', 'disabled');
		$('#border-radius-slider, #switch-size-slider').slider('disable');
		$('#switch-color, #switch-border-color, #active-bg-color').removeAttr('disabled');
		$('#active-switch-color-property, #inactive-switch-color-property').hide();
		$('#switch-color-property').show();
		$('#dual-switch-color').removeAttr('checked').attr('disabled', 'disabled')
		break;
	case 'android': 
		$('#border-radius, #switch-border-color, #active-bg-color').attr('disabled', 'disabled');
		$('#switch-size').removeAttr('disabled');
		$('#border-radius-slider').slider('disable');
		$('#switch-size-slider').slider('enable');
		$('#active-switch-color-property, #inactive-switch-color-property').show();
		$('#switch-color-property').hide();
		$('#dual-switch-color').attr('checked', 'checked').attr('disabled', 'disabled')
		break;
	case 'metro': 
		$('#active-switch-color-property, #inactive-switch-color-property').hide();
		$('#switch-color-property').show();
		$('#switch-size, #switch-color, #switch-border-color, #active-bg-color, #dual-switch-color').removeAttr('disabled');
		$('#switch-size-slider').slider('enable');
		$('#border-radius').attr('disabled', 'disabled')
		$('#border-radius-slider').slider('disable');
		break;
	default: 
		$('#active-switch-color-property, #inactive-switch-color-property').hide();
		$('#switch-color-property').show();
		$('#border-radius, #switch-size, #switch-color, #switch-border-color, #active-bg-color, #dual-switch-color').removeAttr('disabled');
		$('#border-radius-slider, #switch-size-slider').slider('enable');
		break;
	}
}

onoff.resetStyle = function(style){
	stylesChanged = false;
	switch (style) {
	case 'ios4':
		$('#active-bg-color').miniColors('value','#6194FD');
		$('#active-text-color').miniColors('value','#FFFFFF');
		$('#active-text').val('ON');
		$('#inactive-bg-color').miniColors('value','#F8F8F8');
		$('#inactive-text-color').miniColors('value','#666666');
		$('#inactive-text').val('OFF');
		$('#switch-size').val(35);
		$('#switch-size-slider').slider('value', 35);
		$('#dual-switch-color').removeAttr('checked');
		$('#switch-color').miniColors('value','#FFFFFF');
		$('#active-switch-color').miniColors('value','#27A1CA');
		$('#inactive-switch-color').miniColors('value','#A1A1A1');
		$('#switch-border-color').miniColors('value','#666666');
		$('#font-size').val(16);
		$('#font-size-slider').slider('value', 16);
		$('#spacing').val(10);
		$('#spacing-slider').slider('value', 10);
		$('#width').val(90);
		$('#width-slider').slider('value', 90);
		$('#height').val(30);
		$('#height-slider').slider('value', 30);
		$('#border-radius').val(5);
		$('#border-radius-slider').slider('value', 5);
		break;
	case 'ios5':
		$('#active-bg-color').miniColors('value','#6BB2ED');
		$('#active-text-color').miniColors('value','#FFFFFF');
		$('#active-text').val('ON');
		$('#inactive-bg-color').miniColors('value','#FFFFFF');
		$('#inactive-text-color').miniColors('value','#666666');
		$('#inactive-text').val('OFF');
		$('#switch-size').val(30);
		$('#switch-size-slider').slider('value', 30);
		$('#dual-switch-color').removeAttr('checked');
		$('#switch-color').miniColors('value','#FFFFFF');
		$('#active-switch-color').miniColors('value','#27A1CA');
		$('#inactive-switch-color').miniColors('value','#A1A1A1');
		$('#switch-border-color').miniColors('value','#666666');
		$('#font-size').val(16);
		$('#font-size-slider').slider('value', 16);
		$('#spacing').val(15);
		$('#spacing-slider').slider('value', 15);
		$('#width').val(90);
		$('#width-slider').slider('value', 90);
		$('#height').val(30);
		$('#height-slider').slider('value', 30);
		$('#border-radius').val(30);
		$('#border-radius-slider').slider('value', 30);
		break;
	case 'android': 
		$('#active-bg-color').miniColors('value','#C2C2C2');
		$('#active-text-color').miniColors('value','#FFFFFF');
		$('#active-text').val('ON');
		$('#inactive-bg-color').miniColors('value','#C2C2C2');
		$('#inactive-text-color').miniColors('value','#FFFFFF');
		$('#inactive-text').val('OFF');
		$('#switch-size').val(40);
		$('#switch-size-slider').slider('value', 40);
		$('#dual-switch-color').removeAttr('checked');
		$('#switch-color').miniColors('value','#FFFFFF');
		$('#active-switch-color').miniColors('value','#27A1CA');
		$('#inactive-switch-color').miniColors('value','#A1A1A1');
		$('#switch-border-color').miniColors('value','#999999');
		$('#font-size').val(14);
		$('#font-size-slider').slider('value', 14);
		$('#spacing').val(15);
		$('#spacing-slider').slider('value', 15);
		$('#width').val(100);
		$('#width-slider').slider('value', 100);
		$('#height').val(30);
		$('#height-slider').slider('value', 30);
		break;
	case 'metro': 
		$('#active-bg-color').miniColors('value','#2E8DEF');
		$('#active-text-color').miniColors('value','#FFFFFF');
		$('#active-text').val('');
		$('#inactive-bg-color').miniColors('value','#CCCCCC');
		$('#inactive-text-color').miniColors('value','#333333');
		$('#inactive-text').val('');
		$('#switch-size').val(25);
		$('#switch-size-slider').slider('value', 30);
		$('#dual-switch-color').removeAttr('checked');
		$('#switch-color').miniColors('value','#000000');
		$('#active-switch-color').miniColors('value','#27A1CA');
		$('#inactive-switch-color').miniColors('value','#A1A1A1');
		$('#switch-border-color').miniColors('value','#999999');
		$('#font-size').val(14);
		$('#font-size-slider').slider('value', 14);
		$('#spacing').val(10);
		$('#spacing-slider').slider('value', 10);
		$('#width').val(90);
		$('#width-slider').slider('value', 90);
		$('#height').val(30);
		$('#height-slider').slider('value', 30);
		break;
	default: 
		$('#active-bg-color').miniColors('value','#2FCCFF');
		$('#active-text-color').miniColors('value','#FFFFFF');
		$('#active-text').val('ON');
		$('#inactive-bg-color').miniColors('value','#EEEEEE');
		$('#inactive-text-color').miniColors('value','#999999');
		$('#inactive-text').val('OFF');
		$('#switch-size').val(18);
		$('#switch-size-slider').slider('value', 18);
		$('#dual-switch-color').removeAttr('checked');
		$('#switch-color').miniColors('value','#FFFFFF');
		$('#active-switch-color').miniColors('value','#27A1CA');
		$('#inactive-switch-color').miniColors('value','#A1A1A1');
		$('#switch-border-color').miniColors('value','#999999');
		$('#font-size').val(14);
		$('#font-size-slider').slider('value', 14);
		$('#spacing').val(10);
		$('#spacing-slider').slider('value', 10);
		$('#width').val(90);
		$('#width-slider').slider('value', 90);
		$('#height').val(30);
		$('#height-slider').slider('value', 30);
		$('#border-radius').val(20);
		$('#border-radius-slider').slider('value', 20);
		break;
	}
}

onoff.iniGallery = function(){
	
	onoff.gallery = [
		{
			 style: 'custom',
			 activeBgColor: '#2FCCFF',
			 activeTextColor: '#FFFFFF',
			 activeText: '',
			 inactiveBgColor: '#EEEEEE',
			 inactiveTextColor: '#999999',
			 inactiveText: '',
			 switchSize: 15,
			 dualSwitch: false,
			 switchColor: '#FFFFFF',
			 switchActiveColor: '#2FCCFF',
			 switchInactiveColor: '#A1A1A1',
			 borderColor: '#999999',
			 fontSize: 14,
			 spacing: 10,
			 width: 40,
			 height: 5,
			 borderRadius: 20
		},
		{
			 style: 'custom',
			 activeBgColor: '#2FCCFF',
			 activeTextColor: '#FFFFFF',
			 activeText: '',
			 inactiveBgColor: '#EEEEEE',
			 inactiveTextColor: '#999999',
			 inactiveText: '',
			 switchSize: 38,
			 dualSwitch: true,
			 switchColor: '#FFFFFF',
			 switchActiveColor: '#27A1CA',
			 switchInactiveColor: '#A1A1A1',
			 borderColor: '#999999',
			 fontSize: 14,
			 spacing: 10,
			 width: 88,
			 height: 50,
			 borderRadius: 50
		},
		{
			 style: 'custom',
			 activeBgColor: '#2FCCFF',
			 activeTextColor: '#FFFFFF',
			 activeText: '',
			 inactiveBgColor: '#EEEEEE',
			 inactiveTextColor: '#999999',
			 inactiveText: '',
			 switchSize: 20,
			 dualSwitch: true,
			 switchColor: '#FFFFFF',
			 switchActiveColor: '#27A1CA',
			 switchInactiveColor: '#A1A1A1',
			 borderColor: '#999999',
			 fontSize: 14,
			 spacing: 10,
			 width: 60,
			 height: 10,
			 borderRadius: 50
		},
		{
			 style: 'custom',
			 activeBgColor: '#2FCCFF',
			 activeTextColor: '#FFFFFF',
			 activeText: 'ON',
			 inactiveBgColor: '#EEEEEE',
			 inactiveTextColor: '#999999',
			 inactiveText: 'OFF',
			 switchSize: 31,
			 dualSwitch: false,
			 switchColor: '#FFFFFF',
			 switchActiveColor: '#2FCCFF',
			 switchInactiveColor: '#A1A1A1',
			 borderColor: '#999999',
			 fontSize: 18,
			 spacing: 12,
			 width: 86,
			 height: 24,
			 borderRadius: 50
		},
		{
			 style: 'custom',
			 activeBgColor: '#2FCCFF',
			 activeTextColor: '#FFFFFF',
			 activeText: 'ON',
			 inactiveBgColor: '#EEEEEE',
			 inactiveTextColor: '#999999',
			 inactiveText: 'OFF',
			 switchSize: 48,
			 dualSwitch: false,
			 switchColor: '#FFFFFF',
			 switchActiveColor: '#2FCCFF',
			 switchInactiveColor: '#A1A1A1',
			 borderColor: '#FFFFF',
			 fontSize: 40,
			 spacing: 21,
			 width: 180,
			 height: 67,
			 borderRadius: 11
		},
		{
			 style: 'custom',
			 activeBgColor: '#2FCCFF',
			 activeTextColor: '#2FCCFF',
			 activeText: 'ON',
			 inactiveBgColor: '#EEEEEE',
			 inactiveTextColor: '#999999',
			 inactiveText: 'OFF',
			 switchSize: 38,
			 dualSwitch: true,
			 switchColor: '#FFFFFF',
			 switchActiveColor: '#2FCCFF',
			 switchInactiveColor: '#A1A1A1',
			 borderColor: '#FFFFFF',
			 fontSize: 25,
			 spacing: 14,
			 width: 116,
			 height: 41,
			 borderRadius: 50
		},
		{
			 style: 'custom',
			 activeBgColor: '#2FCCFF',
			 activeTextColor: '#FFFFFF',
			 activeText: '',
			 inactiveBgColor: '#EEEEEE',
			 inactiveTextColor: '#999999',
			 inactiveText: '',
			 switchSize: 50,
			 dualSwitch: true,
			 switchColor: '#FFFFFF',
			 switchActiveColor: '#27A1CA',
			 switchInactiveColor: '#4D4D4D',
			 borderColor: '#EEEEEE',
			 fontSize: 14,
			 spacing: 10,
			 width: 112,
			 height: 67,
			 borderRadius: 50
		}
	 ]
	
	$('#random-style').click(function(){
	
		/* INI TO CUSTOM */
		$('#border-radius, #switch-size, #switch-color, #switch-border-color, #active-bg-color, #dual-switch-color').removeAttr('disabled');
		$('#border-radius-slider, #switch-size-slider').slider('enable');
		
		var rand = Math.floor(Math.random()*onoff.gallery.length);
		if(randomStyle === rand) {
			$('#random-style').click();
			return false;
		}
		randomStyle = rand;
		
		$('#style-'+onoff.gallery[rand].style).attr('checked', 'checked')
		$('#active-bg-color').miniColors('value',onoff.gallery[rand].activeBgColor);
		$('#active-text-color').miniColors('value',onoff.gallery[rand].activeTextColor);
		$('#active-text').val(onoff.gallery[rand].activeText);
		$('#inactive-bg-color').miniColors('value',onoff.gallery[rand].inactiveBgColor);
		$('#inactive-text-color').miniColors('value',onoff.gallery[rand].inactiveTextColor);
		$('#inactive-text').val(onoff.gallery[rand].inactiveText);
		$('#switch-size').val(onoff.gallery[rand].switchSize);
		$('#switch-size-slider').slider('value', onoff.gallery[rand].switchSize);
		if(onoff.gallery[rand].dualSwitch) {
			$('#dual-switch-color').attr('checked', 'checked');
			$('#active-switch-color-property, #inactive-switch-color-property').slideDown();
			$('#switch-color-property, #switch-color-property').slideUp();
			$('#active-bg-color').attr('disabled', 'disabled')
		} else {
			$('#dual-switch-color').removeAttr('checked');
			$('#active-switch-color-property, #inactive-switch-color-property').slideUp();
			$('#switch-color-property, #switch-color-property').slideDown();
		}
		$('#switch-color').miniColors('value',onoff.gallery[rand].switchColor);
		$('#active-switch-color').miniColors('value',onoff.gallery[rand].switchActiveColor);
		$('#inactive-switch-color').miniColors('value',onoff.gallery[rand].switchInactiveColor);
		$('#switch-border-color').miniColors('value',onoff.gallery[rand].borderColor);
		$('#font-size').val(onoff.gallery[rand].fontSize);
		$('#font-size-slider').slider('value', onoff.gallery[rand].fontSize);
		$('#spacing').val(onoff.gallery[rand].spacing);
		$('#spacing-slider').slider('value', onoff.gallery[rand].spacing);
		$('#width').val(onoff.gallery[rand].width);
		$('#width-slider').slider('value', onoff.gallery[rand].width);
		$('#height').val(onoff.gallery[rand].height);
		$('#height-slider').slider('value', onoff.gallery[rand].height);
		$('#border-radius').val(onoff.gallery[rand].borderRadius);
		$('#border-radius-slider').slider('value', onoff.gallery[rand].borderRadius);
		
		onoff.renderCss();
		onoff.renderHtml();
		
		return false;
	});
}