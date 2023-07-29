window.onload = function () {
    // Select the elements
    const NAME_SELECTOR = ".sid_girl_title_inner h1 span";
    const ADDRESS_SELECTOR = ".girl-address";
    const PHONE_SELECTOR = ".girl_phone_block_phone";
    const SERVICE_SELECTOR = 'meta[name="description"]';

    const nameElement = document.querySelector(NAME_SELECTOR);

    let addressElement = document.querySelector(ADDRESS_SELECTOR);
    console.log(addressElement);
    let address = 'N/A';

    if (addressElement) {
        // Extract and clean up the street name, zip code, and city
        let blockParts = addressElement.textContent.split('\n');
        let addressParts = blockParts[2].split(',');
        //        addressParts = addressParts.split(',').map(part => part.trim());  // Trim each part
        console.log(blockParts);
        console.log(addressParts);


        // the second last address part is city
        let city = addressParts[addressParts.length - 2];
        // the third last address part is zip code
        let zipCode = addressParts[addressParts.length - 3];
        // the rest is street, it may be empty
        let street = '';
        if (addressParts.length > 3) {
            street = addressParts[addressParts.length - 4];
        } else {
            street = '';
        }

        let anature;
        let ana;
        let cim;
        let cof;

        console.log(street);
        console.log(zipCode);
        console.log(city);

        // check if street is not empty
        if (street) {
            address = `${street}, ${zipCode} ${city}`;
        } else {
            // if no street, address is emtpy
            address = 'Escort';
        }
    }

    let phone = '';
    let phoneElement = document.querySelector(PHONE_SELECTOR);
    if (phoneElement) {
        // Extract the phone number
        phone = phoneElement.textContent.trim();

        // Remove spaces and hyphens
        phone = phone.replace(/[\s-]/g, '');
    }
    // Get the text content
    const name = nameElement ? nameElement.textContent.trim() : 'N/A';

    const keywords = ['Anal mit Schutz', 'Anal Natur', 'COF', 'CIM'];
    let keywordlist = '';
    // Get the service
    const serviceElement = document.querySelector(SERVICE_SELECTOR);
    const service = serviceElement ? serviceElement.getAttribute('content') : 'N/A';
    console.log(service);
    // check if keywords are in service
    if (service) {
        keywords.forEach(keyword => {
            if (service.includes(keyword)) {
                console.log(keyword);
                // store the fonud keyword
                keywordlist = keywordlist + keyword + '  ';
            }
            else {
                console.log('not found');
                keywordlist = keywordlist + '';
            }
        });
    }
    console.log(keywordlist);


    // if keywordlist includes keywords[0] but not keywords[1], add '.' after keywords[0]
    if (keywordlist.includes(keywords[0]) && !keywordlist.includes(keywords[1])) {
        keywordlist = keywordlist.replace(keywords[0], keywords[0] + '.');
    } else if (keywordlist.includes(keywords[1]) && !keywordlist.includes(keywords[0])) {
        // add '.' before keywords[1]
        keywordlist = keywordlist.replace(keywords[1], '.' + keywords[1]);
    }

    // if keywordlist includes CIM but not COF, add mouth emoji after CIM
    if (keywordlist.includes('CIM') && !keywordlist.includes('COF')) {
        keywordlist = keywordlist + '👄';
    } else if (keywordlist.includes('COF') && !keywordlist.includes('CIM')) {
        // add face emoji
        keywordlist = keywordlist + '😮';
    }

    // map keywordlist words to emojis
    keywordlist = keywordlist.replace('Anal mit Schutz', '🍑');
    keywordlist = keywordlist.replace('Anal Natur', '🍑');
    keywordlist = keywordlist.replace('COF', '💦');
    keywordlist = keywordlist.replace('CIM', '💦');


    // Create the overlay
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.left = 0;
    overlay.style.top = '100px';
    overlay.style.width = '30%';
    overlay.style.height = 'calc(50% - 100px)';
    overlay.style.backgroundColor = 'rgba(0,0,0,0.7)';
    overlay.style.color = 'white';
    overlay.style.display = 'flex';
    overlay.style.justifyContent = 'center';
    overlay.style.alignItems = 'center';
    overlay.style.zIndex = 10000;
    overlay.style.fontSize = '1em';

    // Set the overlay text
    let icon = address === 'Escort' ? '🚗' : '🛌';
    overlay.innerHTML = `
    <div>
        <p>${name}</p>
        <p>${icon}   ${keywordlist}</p>
        <p style="margin-left: 1em; font-size: 0.8em;">${address}</p>
        <p style="margin-left: 1em; font-size: 0.8em;">${phone}</p>
    </div>
`;

    // Add the overlay to the body
    document.body.appendChild(overlay);
};
