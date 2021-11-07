$().ready(function(){
	$('#copy-button').on('click', function(){		
		$('#key-value').select();
		document.execCommand("copy");
	});

	$('#remember').on('click', function(e){
		e.preventDefault();
		var firstRotor = $('select#firstRotor').val();
		if(firstRotor == null){
			firstRotor = '-';
		}
		var secondRotor = $('select#secondRotor').val();
		if(secondRotor == null){
			secondRotor = '-';
		}
		var thirdRotor = $('select#thirdRotor').val();
		if(thirdRotor == null){
			thirdRotor = '-';
		}
		$('#key-value').val(' '+firstRotor+' '+':'+' '+secondRotor+' '+':'+' '+thirdRotor+' ');
	});

	$('#process_but').on('click', function(e){
		e.preventDefault();
		var firstRotor = $('select#firstRotor').val();
		var secondRotor = $('select#secondRotor').val();
		var thirdRotor = $('select#thirdRotor').val();
		var inputText = $('#inputText').val();
		var mode = $('input[name="mode"]:checked').val();
	
		if(firstRotor !== null & secondRotor !== null & thirdRotor !== null & inputText !== null & mode !== null){
			process(firstRotor, secondRotor, thirdRotor, inputText, mode);
		}else{
			alert('No input text or no rotors settings');
		}
	});
});

async function process(firstRotor, secondRotor, thirdRotor, inputText, mode){
	let data = {
	  action: mode,
	  frtRrStart: firstRotor,
	  sndRrStart: secondRotor,
	  trdRrStart: thirdRotor,
	  inputString: inputText
	} 

	let request = await fetch('/',
  	{
	    body: JSON.stringify(data),
	    method: "POST",
	    headers: { 'Content-Type': 'application/json' }
	  });
	  let res = await request.text();
	//let res = await eel.process(firstRotor, secondRotor, thirdRotor, inputText, mode)();
	document.getElementById('output-text').innerHTML = res;	
}