
<template>
  <div class="sidebar" :class="{ collapsed: isCollapsed }">
    <div class="sidebar-header">
      <button @click="newChat" class="new-chat-btn">
        <span v-if="!isCollapsed">{{ $t('newChat') }}</span>
        <span v-else>+</span>
      </button>
      <div class="sidebar-actions">
        <div class="language-switcher" v-click-outside="closeLanguageMenu">
          <button @click="toggleLanguageMenu" class="language-btn">🌐</button>
          <ul v-if="showLanguageMenu" class="language-menu">
            <li @click="switchLanguage('en')">
              <span class="check-mark"><span v-if="currentLocale === 'en'">✔️</span></span> <span class="lang-text">English</span>
            </li>
            <li @click="switchLanguage('zh-CN')">
              <span class="check-mark"><span v-if="currentLocale === 'zh-CN'">✔️</span></span> <span class="lang-text">简体中文</span>
            </li>
            <li @click="switchLanguage('zh-TW')">
              <span class="check-mark"><span v-if="currentLocale === 'zh-TW'">✔️</span></span> <span class="lang-text">繁體中文</span>
            </li>
          </ul>
        </div>
        <button @click="toggleSidebar" class="collapse-btn">☰</button>
      </div>
    </div>
    <ul>
      <li v-for="chat in chats" :key="chat.id" :class="{ 'active-chat': String(chat.id) === router.currentRoute.value.params.id }">
        <router-link :to="`/chats/${chat.id}`" class="chat-link">{{ chat.name }}</router-link>
        <div class="chat-actions" v-if="!isCollapsed">
          <button @click="renameChat(chat)" class="action-btn" :title="$t('rename')">✏️</button>
          <button @click="removeChat(chat.id)" class="action-btn" :title="$t('delete')">🗑️</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import { useChatStore } from '../store'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const store = useChatStore()
const router = useRouter()
const { t, locale } = useI18n()

const chats = computed(() => store.chats)
const currentLocale = computed(() => locale.value)
const showLanguageMenu = ref(false)

onMounted(() => {
  store.fetchChats()
})

const newChat = async () => {
  const newChat = await store.createNewChat()
  router.push(`/chats/${newChat.id}`)
}

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}

const isCollapsed = ref(false)

const renameChat = async (chat) => {
  const newName = prompt(t('enterNewChatName'), chat.name);
  if (newName && newName.trim() !== '') {
    await store.updateChatName(chat.id, newName.trim());
  }
}

const removeChat = async (chatId) => {
  if (confirm(t('deleteChatConfirmation'))) {
    await store.deleteChat(chatId);
    // If the current chat is deleted, navigate away
    if (router.currentRoute.value.params.id === String(chatId)) {
      router.push('/');
    }
  }
}

const toggleLanguageMenu = () => {
  showLanguageMenu.value = !showLanguageMenu.value
}

const closeLanguageMenu = () => {
  showLanguageMenu.value = false
}

const switchLanguage = (lang) => {
  locale.value = lang
  document.cookie = `locale=${lang};path=/;max-age=31536000` // 1 year
  showLanguageMenu.value = false
}

const vClickOutside = {
  beforeMount(el, binding) {
    el.clickOutsideEvent = function(event) {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event, el);
      }
    };
    document.body.addEventListener('click', el.clickOutsideEvent);
  },
  unmounted(el) {
    document.body.removeEventListener('click', el.clickOutsideEvent);
  },
};
</script>

<style scoped>
.sidebar {
  width: 250px;
  background-color: #f0f0f0;
  padding: 20px;
  transition: width 0.3s ease;
  display: flex;
  flex-direction: column;
}

.sidebar.collapsed {
  width: 80px;
  padding: 20px 10px;
}

.sidebar.collapsed .chat-link {
  justify-content: center;
}

.sidebar.collapsed .chat-link,
.sidebar.collapsed .new-chat-btn span {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.sidebar-actions {
  display: flex;
  align-items: center;
}

.language-switcher {
  position: relative;
  margin-right: 10px;  
}

.language-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2em;
}

.language-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  list-style: none;
  padding: 5px 0;
  margin: 0;
  z-index: 100;
  min-width: 120px;
}

.language-menu li {
  padding: 8px 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  white-space: nowrap;
}

.language-menu li:hover {
  background-color: #f0f0f0;
}

.language-menu li .check-mark {
  display: inline-block;
  width: 20px;
  text-align: center;
  margin-right: 5px;
}

.language-menu li .lang-text {
  margin-left: 0.5em;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
  overflow-y: auto;
}

.sidebar li {
  display: flex;
  align-items: center;
  
  margin-bottom: 10px;
  border-radius: 5px;
  padding: 5px;
}

.sidebar li:hover {
  background-color: #e0e0e0;
}

.active-chat {
  background-color: #cce5ff;
  border-left: 4px solid #007bff;
}

.active-chat .chat-link {
  font-weight: bold;
}

.chat-link {
  flex-grow: 1;
  text-decoration: none;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 2px 5px;
  visibility: hidden;
}

.sidebar li:hover .action-btn {
  visibility: visible;
}
</style>

