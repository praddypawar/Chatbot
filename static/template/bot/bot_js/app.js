
const chatButton = document.querySelector('.chatbox__button');
const chatContent = document.querySelector('.chatbox__support');
const icons = {
    isClicked: '<img src="../../static/template/bot/bot_images/chat-icon.png" />',
    isNotClicked: '<img src="../../static/template/bot/bot_images/chat-icon.png" />'
}
const chatbox = new InteractiveChatbox(chatButton, chatContent, icons);
chatbox.display();
chatbox.toggleIcon(false, chatButton);
