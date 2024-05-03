let n2 = 0;
let n3 = 0;
let n4 = 0;
let n5 = 0;
let n6 = 0;



let fragment = new DocumentFragment();

let s = document.createElement('h1');
s.innerHTML = document.querySelector('h1').innerHTML;
s.className = 'title_lv1';
fragment.appendChild(s);

let titres = document.querySelectorAll('h2,h3,h4,h5,h6');

for (let titre of titres){
		
	// création du lien vers le titre
	
	let lien = document.createElement('p');
	
	// affectation d'une classe CSS/puce selon le niveau du titre	
	switch (titre.tagName){
		
		case 'H2':
			n3 = 0; // variables gérant
			n4 = 0; // les différents niveaux
			n2 += 1; // de la numérotation
			n = n2.toString() + '.'; // construction de l'id du titre ET de la numérotation du lien
			titre.id = n; // affectation de l'id au titre
			titre.innerHTML = n + ' ' + titre.innerHTML; // un p'tit espace entre la numérotation et le titre lui-même
			lien.innerHTML = '&#128194; <a href=#' + n + '>' + titre.innerHTML + '</a>'; // le texte du lien
			lien.className = 'title_lv2'; // affectation de sa classe au lien
			break;
		case 'H3':
			n4 = 0;
			n3 += 1;
			n = n2.toString() +'.' + n3.toString() + '.';
			titre.id = n; 
			titre.innerHTML = n + ' ' + titre.innerHTML;
			lien.innerHTML = '&#128450; <a href=#' + n + '>' + titre.innerHTML + '</a>';
			lien.className = 'title_lv3';
			break;
		case 'H4':
			n5 = 0;
			n4 += 1;
			n = n2.toString() +'.' + n3.toString() +'.' + n4.toString() + '.';
			titre.id = n; 
			titre.innerHTML = n + ' ' + titre.innerHTML;
			//lien.innerHTML = '&#128466; <a href=#' + n + '>' + titre.innerHTML + '</a>';
			//lien.className = 'title_lv4';
			break;
		case 'H5':
			n6 = 0;
			n5 += 1;
			n = n2.toString() +'.' + n3.toString() +'.' + n4.toString() + '.' + n5.toString() + '.';
			titre.id = n; 
			titre.innerHTML = n + ' ' + titre.innerHTML;
			//lien.innerHTML = '&#x2023; <a href=#' + n + '>' + titre.innerHTML + '</a>';
			//lien.className = 'title_lv5';
			break;
		case 'H6':
			n6 += 1;
			n = n2.toString() +'.' + n3.toString() +'.' + n4.toString() + '.' + n5.toString() + '.' + n6.toString() + '.';
			titre.id = n; 
			titre.innerHTML = n + ' ' + titre.innerHTML;
			//lien.innerHTML = '<a href=#' + n + '>' + titre.innerHTML + '</a>';
			//lien.className = 'title_lv6';
			break;
	}
	
	// ajout du lien au sommaire
	if (lien !== null){
		fragment.appendChild(lien);
	}
	
}


document.getElementById('sommaire').appendChild(fragment);
