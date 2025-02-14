# Dify迁移

以下操作均在DIFY-MAIN --> web文件 下执行

### 国际化

**i18n的文件夹里面的每个文件去修改他有关于dify的相关文字**

**或者直接将国际化删了**

**i18n\README.md\:79**

**除了简体中文剩下的都删了**

```js
export const languages = [
  {
    value: 'en-US',
    name: 'English(United States)',
    example: 'Hello, 智定义!',
    supported: true,
  },
  {
    value: 'zh-Hans',
    name: '简体中文',
    example: '你好，Dify！',
    supported: true,
  },
  {
    value: 'pt-BR',
    name: 'Português(Brasil)',
    example: 'Olá, Dify!',
    supported: true,
  },
  {
    value: 'es-ES',
    name: 'Español(España)',
    example: 'Saluton, Dify!',
    supported: false,
  },
  {
    value: 'fr-FR',
    name: 'Français(France)',
    example: 'Bonjour, Dify!',
    supported: false,
  },
  {
    value: 'de-DE',
    name: 'Deutsch(Deutschland)',
    example: 'Hallo, Dify!',
    supported: false,
  },
  {
    value: 'ja-JP',
    name: '日本語(日本)',
    example: 'こんにちは、Dify!',
    supported: false,
  },
  {
    value: 'ko-KR',
    name: '한국어(대한민국)',
    example: '안녕, Dify!',
    supported: true,
  },
  {
    value: 'ru-RU',
    name: 'Русский(Россия)',
    example: ' Привет, Dify!',
    supported: false,
  },
  {
    value: 'it-IT',
    name: 'Italiano(Italia)',
    example: 'Ciao, Dify!',
    supported: false,
  },
  {
    value: 'th-TH',
    name: 'ไทย(ประเทศไทย)',
    example: 'สวัสดี Dify!',
    supported: false,
  },
  {
    value: 'id-ID',
    name: 'Bahasa Indonesia',
    example: 'Saluto, Dify!',
    supported: false,
  },
  {
    value: 'uk-UA',
    name: 'Українська(Україна)',
    example: 'Привет, Dify!',
    supported: true,
  },
  // Add your language here 👇
  ...
  // Add your language here 👆
]
```



### 修改请求地址

**.env.example**

```js
NEXT_PUBLIC_API_PREFIX=http://183.201.231.29:2580/console/api
NEXT_PUBLIC_PUBLIC_API_PREFIX=http://183.201.231.29:2580/api
```

**dify-main\web\config\index.ts**

```js
apiPrefix = 'http://183.201.231.29:2580/console/api'
publicApiPrefix = 'http://183.201.231.29:2580/api' // avoid browser private mode api cross origin
```

### 替换logo

**dify-mainlweblapp\componentslbase\logo\logo-site.tsx**

```js
const src = theme === 'light' ? '/logo/logo-site.png' : `/logo/logo-site-${theme}.png` 
替换成自己的logo
```

### 去除github

**dify-main\web\app\(commonLayout)\apps\page.tsx**

**注释掉**

```js
 <footer className='px-12 py-6 grow-0 shrink-0'>
        <h3 className='text-xl font-semibold leading-tight text-gradient'>{t('join')}</h3>
        <p className='mt-1 text-sm font-normal leading-tight text-gray-700'>{t('communityIntro')}</p>
        <div className='flex items-center gap-2 mt-3'>
          <a className={style.socialMediaLink} target='_blank' rel='noopener noreferrer' href='https://github.com/langgenius/dify'><span className={classNames(style.socialMediaIcon, style.githubIcon)} /></a>
          <a className={style.socialMediaLink} target='_blank' rel='noopener noreferrer' href='https://discord.gg/FngNHpbcY7'><span className={classNames(style.socialMediaIcon, style.discordIcon)} /></a>
        </div>
      </footer>

```

### **删除 探索**

**dify-main/web/app/components/header/index.tsx:75:9:div**

**注释掉**

```js
   {!isCurrentWorkspaceDatasetOperator && <ExploreNav className={navClassName} />}
```

### 删除 探索DIfy的应用

**dify-main/web/app/components/explore/app-list/index.tsx:168:11:div**

**注释掉**

```js
 {pageType === PageType.EXPLORE && (
        <div className='shrink-0 pt-6 px-12'>
          <div className={`mb-1 ${s.textGradient} text-xl font-semibold`}>{t('explore.apps.title')}</div>
          <div className='text-gray-500 text-sm'>{t('explore.apps.description')}</div>
        </div>
      )}
```

### **删除** 知识库-知道吗

**dify-main/web/app/(commonLayout)/datasets/DatasetFooter.tsx:9:5:footer**

```js
<footer className='px-12 py-6 grow-0 shrink-0'>
      <h3 className='text-xl font-semibold leading-tight text-gradient'>{t('dataset.didYouKnow')}</h3>
      <p className='mt-1 text-sm font-normal leading-tight text-gray-700'>
        {t('dataset.intro1')}<span className='inline-flex items-center gap-1 text-blue-600'>{t('dataset.intro2')}</span>{t('dataset.intro3')}<br />
        {t('dataset.intro4')}<span className='inline-flex items-center gap-1 text-blue-600'>{t('dataset.intro5')}</span>{t('dataset.intro6')}
      </p>
</footer>
```

**替换为**

```js
   <></>
```

### 替换 工具 - 你有兴趣成为DIfy贡献工具

**dify-main/web/app/components/tools/provider/contribute.tsx:30:9:div**

```js
    <a
      href='https://github.com/langgenius/dify/blob/main/api/core/tools/README.md'
      target='_blank'
      rel='noopener noreferrer'
      className="group flex col-span-1 bg-white bg-cover bg-no-repeat bg-[url('~@/app/components/tools/provider/grid_bg.svg')] border-2 border-solid border-transparent rounded-xl shadow-sm min-h-[160px] flex-col transition-all duration-200 ease-in-out cursor-pointer hover:shadow-lg"
    >
      <div className='flex pt-[14px] px-[14px] pb-3 h-[66px] items-center gap-3 grow-0 shrink-0'>
        <div className='relative shrink-0 flex items-center'>
          <div className='z-10 flex p-3 rounded-[10px] bg-white border-[0.5px] border-primary-100 shadow-md'><RiHammerFill className='w-4 h-4 text-primary-600'/></div>
          <div className='-translate-x-2 flex p-3 rounded-[10px] bg-[#FEF6FB] border-[0.5px] border-[#FCE7F6] shadow-md'><Heart02 className='w-4 h-4 text-[#EE46BC]'/></div>
        </div>
      </div>
      <div className='mb-3 px-[14px] text-[15px] leading-5 font-semibold'>
        <div className='text-gradient'>{t('tools.contribute.line1')}</div>
        <div className='text-gradient'>{t('tools.contribute.line2')}</div>
      </div>
      <div className='px-4 py-3 border-t-[0.5px] border-black/5 flex items-center space-x-1 text-[#155EEF]'>
        <BookOpen01 className='w-3 h-3' />
        <div className='grow leading-[18px] text-xs font-normal'>{t('tools.contribute.viewGuide')}</div>
        <ArrowUpRight className='w-3 h-3' />
      </div>
    </a>
```

**替换为**

```js
  <></>
```

### 浏览器标签显示

**web\app\(commonLayout)\apps\hooks\Apps.tsx**

剩下的同理 根据名称去找他国际化的字段在通过国际化的字段进行搜索查看修改

全局搜索 Dify 替换为 智定义

 dify-main\web\app\(commonLayout)\layout.tsx

dify-mainlwebapp\(commonLayout)\datasetslpage.tsx

dify-mainlwebapp\(commonLayout)\datasets\Datasets.tsx

dify-main\web\app\(commonLayout)\datasets\(datasetDetailLayout)\[datasetld]Vlayout.tsx

dify-main\webapp\(commonLayout)\tools\page.tsx

dify-mainlwebapp\account\layout.tsx

dify-mainlwebapplcomponents\base\chat\chat-with\historyindex.tsx
dify-main\weblapp\components\base\chatlembedded

```jsx
  useEffect(() => {
    document.title = `${t('common.menus.apps')} -  智定义`
    if (localStorage.getItem(NEED_REFRESH_APP_LIST_KEY) === '1') {
      localStorage  .removeItem(NEED_REFRESH_APP_LIST_KEY)
      mutate()
    }
  }, [mutate, t])
```



### 我的账户 消除dify账号

**dify-main/web/app/account/account-page/index.tsx:174:9:div**

```js
<div className={titleClassName}>{t('common.account.langGeniusAccount')}</div>
<div className={descriptionClassName}>{t('common.account.langGeniusAccountTip')}</div>
```

**在每个国际化文件中寻找 common.ts文件 修改 **

```js
langGeniusAccount: '账号',
langGeniusAccountTip: '账号和相关的用户数据。',
```

### 删除 帮助文档

**dify-mainlwebapplcomponents\header\account-dropdown\index.tsx**

**注释**

```js
  <Menu.Item>
                      <Link
                        className={classNames(itemClassName, 'group justify-between')}
                        href={
                          locale !== LanguagesSupported[1] ? 'https://docs.dify.ai/' : `https://docs.dify.ai/v/${locale.toLowerCase()}/`
                        }
                        target='_blank' rel='noopener noreferrer'>
                        <div>{t('common.userProfile.helpCenter')}</div>
                        <ArrowUpRight className='hidden w-[14px] h-[14px] text-gray-500 group-hover:flex' />
                      </Link>
                    </Menu.Item>
```

### 删除国际化

 **dify_zdy/web/app/components/base/select/locale.tsx:23:9:div**

```js 
<Menu as="div" className="relative inline-block text-left">
        <div>
          <Menu.Button className="inline-flex w-full h-[44px]justify-center items-center
          rounded-lg px-[10px] py-[6px]
          text-gray-900 text-[13px] font-medium
          border border-gray-200
          hover:bg-gray-100">
            <GlobeAltIcon className="w-5 h-5 mr-1" aria-hidden="true" />
            {item?.name}
          </Menu.Button>
        </div>
        <Transition
          as={Fragment}
          enter="transition ease-out duration-100"
          enterFrom="transform opacity-0 scale-95"
          enterTo="transform opacity-100 scale-100"
          leave="transition ease-in duration-75"
          leaveFrom="transform opacity-100 scale-100"
          leaveTo="transform opacity-0 scale-95"
        >
          <Menu.Items className="absolute right-0 mt-2 w-[200px] origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-10">
            <div className="px-1 py-1 ">
              {items.map((item) => {
                return <Menu.Item key={item.value}>
                  {({ active }) => (
                    <button
                      className={`${active ? 'bg-gray-100' : ''
                      } group flex w-full items-center rounded-lg px-3 py-2 text-sm text-gray-700`}
                      onClick={(evt) => {
                        evt.preventDefault()
                        onChange && onChange(item.value)
                      }}
                    >
                      {item.name}
                    </button>
                  )}
                </Menu.Item>
              })}
            </div>

          </Menu.Items>
        </Transition>
      </Menu> 
```
