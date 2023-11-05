function buttonClicked(airline) {
    console.log('Button clicked for', airline);
    if (airline === 'American Airlines') {
        window.location.href = '/confirmation';
    } else if (airline === 'Delta Airlines') {
        window.location.href = '/confirmation';
    } else if (airline === 'Southwest Airlines') {
        window.location.href = '/confirmation';
    } else if (airline === 'Spirit Airlines') {
        window.location.href = '/confirmation';
    } else if (airline === 'Frontier Airlines') {
        window.location.href = '/confirmation';
    } else if (airline === 'Alaska Airlines') {
    window.location.href = '/confirmation';
    } else if (airline === 'British Airways') {
        window.location.href = '/confirmation';
    }else if (airline === 'Allegiant Airways') {
        window.location.href = '/confirmation';
    }
    // Add more conditions for other airlines as needed
    
}
