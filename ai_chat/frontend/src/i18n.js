import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import zhCN from './locales/zh-CN.json'
import zhTW from './locales/zh-TW.json'

const messages = {
  en,
  'zh-CN': zhCN,
  'zh-TW': zhTW
}

function getInitialLocale() {
  const cookieLocale = document.cookie.split('; ').find(row => row.startsWith('locale='))
  if (cookieLocale) {
    return cookieLocale.split('=')[1]
  }

  const browserLocale = navigator.language
  if (messages.hasOwnProperty(browserLocale)) {
    return browserLocale
  }

  return 'en'
}

const i18n = createI18n({
  legacy: false,
  locale: getInitialLocale(),
  fallbackLocale: 'en',
  messages
})

export default i18n
