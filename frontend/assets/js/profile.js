async function getImageResponse(event) {
    loadPreviewImage(event);
    result = await submitImage();

    let response = await result.json();
    if (result.status == 201) {
        alert(response["message"]);
        const path = response["path"]
        const imageInput = document.querySelector(".image")
        imageInput.setAttribute("value", path);
    } else {
        alert(JSON.stringify(response));
    }
}

function loadPreviewImage(event) {
    var reader = new FileReader();
    reader.onload = function (event) {
        var img = document.createElement("img");
        img.setAttribute("src", event.target.result);
        document.querySelector("div#preview-image").appendChild(img);
    };
    reader.readAsDataURL(event.target.files[0]);
}

async function submitImage() {
    const fileInput = document.querySelector(".imagefile");
    const formData = new FormData();

    var myHeaders = new Headers();
    myHeaders.append(
        "Authorization",
        "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjY4OTMwMDA2LCJqdGkiOiIwOTU3NDAxNi04YmE2LTQyZjgtODhhZC0wYTkzMzBjNTY5N2UiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiXHViYmZjXHVjMjE4IiwibmJmIjoxNjY4OTMwMDA2LCJleHAiOjE2NjkwMTY0MDZ9.LnixDrHFAMusZhMSc2vIsfru4D61UAMrIx9ca3kTX3c"
    )

    formData.append("image", fileInput.files[0])

    var requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: formData,
    };

    const result = await fetch(
        "http://127.0.0.1:5000/upload/profile/image/",
        requestOptions
    )

    return result;
}

function getFormJson() {
    let form = document.querySelector("#profile-form");
    let data = new FormData(form);
    let serializedFormData = serialize(data);
    return JSON.stringify(serializedFormData);
  }
  
  /**
   * form 태그 안에 있는 내용을 dictionary 형태로 반환합니다.
   */
  function serialize(rawData) {
    let serializedData = {};
    for (let [key, value] of rawData) {
      console.log(value);
      if (key == "imagefile") {
        continue;
      }
      if (value == "") {
        serializedData[key] = null;
      }
      serializedData[key] = value;
    }
    console.log(serializedData);
    return serializedData;
  }
  
  /**
   * 정제된 데이터를 넣어 프로필 수정 요청을 보냅니다.
   */
  async function submitProfileData() {
    // 인증을 위한 header 설정
    var myHeaders = new Headers();
    myHeaders.append(
      "Authorization",
      "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjY4OTMwMDA2LCJqdGkiOiIwOTU3NDAxNi04YmE2LTQyZjgtODhhZC0wYTkzMzBjNTY5N2UiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiXHViYmZjXHVjMjE4IiwibmJmIjoxNjY4OTMwMDA2LCJleHAiOjE2NjkwMTY0MDZ9.LnixDrHFAMusZhMSc2vIsfru4D61UAMrIx9ca3kTX3c"
    );
    myHeaders.append("Content-Type", "application/json");
  
    // 보낼 데이터 설정
    var raw = getFormJson();
  
    // 최종 옵션 설정
    var requestOptions = {
      method: "PUT",
      headers: myHeaders,
      body: raw,
      redirect: "follow",
    };
  
    // 프로필 정보 수정 요청
    const response = await fetch(
      "http://127.0.0.1:5000/mypage/4/",
      requestOptions
    );
    console.log(response.status);
    if (response.status == 200) {
      // window.location.href = "http://localhost:3000/flastagram/posts/";
      alert(JSON.stringify(await response.json()));
    } else {
      alert(JSON.stringify(await response.json()));
    }
  }