const postListBaseUrl = "http://127.0.0.1:5000/posts/";

async function getPostListDatafromAPI() {
    try {
        const somePromise = await fetch(postListBaseUrl);
        const result = somePromise.json();
        return result;
    } catch (error) {
        console.log(error);
    }
}

function copyDiv() {
    const postDiv = document.querySelector(".post");
    const newNode = postDiv.cloneNode(true);
    newNode.id = "copied-posts";
    postDiv.after(newNode);
}

function loadPosts() {
    getPostListDatafromAPI()
        .then((result) => {
            for (let i = 0; i < result.length; i++) {
                copyDiv();
                const authorNameElements = document.querySelectorAll(".author");
                for (const authorName in authorNameElements) {
                    authorNameElements[authorName].innerText =
                        result[result.length - 1 - i]["author_name"];
                }
                const titleElement = document.querySelector(".title");
                titleElement.innerText = result[result.length - 1 - i]["title"];
                const contentElement = document.querySelector(".content");
                contentElement.innerText = result[result.length - 1 - i]["content"];
                if (i == 0) {
                    document.getElementById("copied-posts").style.display = "none";
                }
            }
        })
        .catch((error) => {
            console.log(error);
        })
}
loadPosts();