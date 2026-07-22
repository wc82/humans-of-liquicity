document
.getElementById("storyForm")
.addEventListener("submit", async e => {

e.preventDefault();

let body = `
NAME:
${name.value}

CITY:
${city.value}

FIRST LIQUICITY FESTIVAL:
${festival.value}

TRACK:
${track.value}

MESSAGE:
${message.value}

IMAGE:
${document.getElementById("image").files[0]?.name}
`;

let title =
"Human: " + name.value;


await fetch(
"https://api.github.com/repos/wc82/humans-of-liquicity/issues",
{
method:"POST",
headers:{
"Accept":"application/vnd.github+json"
},
body:JSON.stringify({
title:title,
body:body
})
}
);


alert(
"Thank you! Your Humans of Liquicity story has been submitted."
);

});
