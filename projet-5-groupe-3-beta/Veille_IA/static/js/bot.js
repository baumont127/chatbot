
function getBotResponse(){
          
    /* recupération demande utilisateur*/
      var myText = $("#my-text").val(); 
      var userBubble = '<div class="your-container"><div class="your-msg">'+ myText +'</div></div>';
      $("#my-text").val("");
      $(".chat-view").append(userBubble);
      $(".chat-view").stop().animate({scrollTop: $(".chat-view")[0].scrollHeight}, 1000);
      let formData = new FormData()
      formData.append('msg', myText)

      let csrfTokenValue = document.querySelector('[name=csrfmiddlewaretoken]').value;
      const request = new Request('/get_bot_response', {method: 'POST', body: formData, headers: {'X-CSRFToken': csrfTokenValue}});
      fetch(request)
            .then(response => response.json())
            .then(result => {
                    for (let i = 0; i < result["operation_result"].length; i++) {
                        
                        if (result["operation_result"][i]["titre"] == "Vous n'avez pas encore de ressource" || result["operation_result"][i]["titre"] == "Veuillez précisser votre demande") {
                            let botBubble = '<div class="bot-container"><div class="bot-msg">'+ result["operation_result"][i]["titre"] +'</div></div>';
                            $(".chat-view").append(botBubble);
                            $(".chat-view").stop().animate({scrollTop: $(".chat-view")[0].scrollHeight}, 1000);
                            $(document).ready( function() {
                                $("#circle1").css({ background:'linear-gradient(rgba(255, 255, 255, 0.9), #ff0000)'});
                                $("#circle2").css({ background:'linear-gradient(rgba(255, 255, 255, 0.9), #ff0000)'});
                        });
                        } 
                        else {
                        let botBubble = '<div class="bot-container"><div class="bot-msg">'+ result["operation_result"][i]['titre'] + " : " + '<a href=' + result["operation_result"][i]['lien'] + ">" + result["operation_result"][i]['lien'] + "</a>" +'</div></div>';
                        $(".chat-view").append(botBubble);
                        $(".chat-view").stop().animate({scrollTop: $(".chat-view")[0].scrollHeight}, 1000);
                        $(document).ready( function() {
                            $("#circle1").css({ background:'linear-gradient(rgba(255, 255, 255, 0.9), #1aacf0)'});
                            $("#circle2").css({ background:'linear-gradient(rgba(255, 255, 255, 0.9), #1aacf0)'});
                    });
                    }
                    }

            })                   
  }
