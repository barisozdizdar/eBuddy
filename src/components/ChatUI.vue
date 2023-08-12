<template>
  <div class="chatbot-container">
    <div class="chatbot-header-container">
      <div class="chatbot-header">E-Buddy</div>
      <img src="https://www.khas.edu.tr/wp-content/uploads/2022/06/khas-logo-test.png" alt="Kadir Has Üniversitesi" data-mobile="https://www.khas.edu.tr/wp-content/uploads/2022/02/khas-logo-test.png">
    </div>
    <div class="chatbot-body-container">
      <div class="chatbot-body" ref="chatbotBody">
        <div class="messages" ref="messages">
          <div v-for="(message, index) in messages" :key="index">
            <div v-if="message.isBot" class="bot-message">{{ message.text }}              </div>
            <div v-else class="user-message">{{ message.text }}</div>
            </div>
          </div>
          <div class="scroll-bottom-button" @click="scrollToBottom">
            <i class="fas fa-arrow-circle-down"></i>
          </div>
      </div>
      <div class="input-container">
        <div class="input">
          <input v-model="currentMessage" @keyup.enter="sendMessage" placeholder="Type a message...">
          <button @click="sendMessage">Send</button>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      messages: [],
      currentMessage: ''
    };
  },
  methods: {
    sendMessage() {
      if (this.currentMessage) {
        this.messages.push({
          text: this.currentMessage,
          isBot: false
        });

        this.fakeBotResponse(this.currentMessage);
        this.currentMessage = '';
        this.$nextTick(() => {
          this.scrollBottom();
        });
      }
    },
    fakeBotResponse(messageFromUser) {
      if (messageFromUser) {
        const data = JSON.stringify({
          question: messageFromUser
        });

        const config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: 'http://localhost:8000/question',
          headers: {
            accept: 'application/json',
            'Content-Type': 'application/json'
          },
          data: data
        };

        axios
          .request(config)
          .then((response) => {
            console.log(JSON.stringify(response.data));
            
            this.messages.push({
            text: response.data.trim(),
            isBot: true
            });
            this.currentMessage = '';
            this.$nextTick(() => {
              this.scrollBottom();
            });
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
    scrollBottom() {
      const chatbotBody = this.$refs.chatbotBody;
      chatbotBody.scrollTop = chatbotBody.scrollHeight;
    }
  }
};

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Lato&display=swap');
@import url('https://fonts.cdnfonts.com/css/maximum-impact');
.chatbot-container {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chatbot-header-container {
  font-family: 'Maximum Impact', sans-serif;
  font-size: 25px;
  font-weight: 300;
  line-height: 1.7em;
  height: 50px;
  background-color: #ffffff;
  color: #00529B;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

img {
  margin-bottom: 0px;
  max-width: 15%;
  max-height: 50px;
  position: absolute;
  left: 20px;
}

.chatbot-body-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  position: relative; 
}

.chatbot-body {
  width: 100%;

  overflow-y: auto;
  position: absolute; 
  top: 0; 
  left: 0; 
  bottom: 100px;
}


.messages {
  width:100%;
  padding: 16px;
}

.bot-message {
  background-color: #87CEFA;
  color: #000000;
  padding: 8px;
  border-radius: 8px;
  margin-bottom: 8px;
  margin-left: 50px; 
  position: relative; 
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  word-wrap: break-word;
}

.bot-message::before {
  content: "";
  position: absolute;
  top: 0;
  left: -50px; 
  width: 40px; 
  height: 40px; 
  background-image: url("https://ww1.freelogovectors.net/wp-content/uploads/2020/07/kadir-has-universitesi-logo.png?lossy=1&w=2560&ssl=1");
  background-size: cover;
  border-radius: 50%;
}


.user-message {
  background-color: #F5F5F5;
  color: #000000;
  padding: 8px;
  border-radius: 8px;
  margin-bottom: 8px;
  position: relative;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  word-wrap: break-word;
}

.input-container {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: -1px;
}

.input {
  width: 100%;
  max-width: 600px;
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
  background-color: #fff;
  border-top: 1px solid #eee;
  border-radius: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}


.input input {
  font-family: 'Lato', sans-serif;
  flex: 1;
  margin-right: 16px;
  padding: 8px;
  border-radius: 8px;
  border: none;
}

.input button {
  font-family: 'Lato', sans-serif;
  padding: 8px;
  border-radius: 8px;
  border: none;
  background-color: #0693e3;
  color: #fff;
  cursor: pointer;
}

  
.input button:hover {
  background-color: #00529B;
}

::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}
  
::-webkit-scrollbar-thumb:hover {
  background: #555;
}  

.scroll-bottom-button {
  position: fixed;
  bottom: 90px;
  right: 20px;
  z-index: 999;
  width: 40px;
  height: 40px;
  background-color: #0693e3;
  color: #fff;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 20px;
  transition: background-color 0.3s ease;
}

.scroll-bottom-button:before {
  content: '\2193';
  display: block;
  text-align: center;
  line-height: 40px;
}

.scroll-bottom-button:hover {
  background-color: #00529B;
}
</style>
