'use client'
import type { FC } from 'react'
import classNames from '@/utils/classnames'
import { useSelector } from '@/context/app-context'

type LogoSiteProps = {
  className?: string
}

const LogoSite: FC<LogoSiteProps> = ({
  className,
}) => {
  const { theme } = useSelector((s) => {
    return {
      theme: s.theme,
    }
  })

  const src = theme === 'light' ? '/logo/logo-site.png' : `/logo/logo-site-${theme}.png`
  return (
    // <img
    //   src={src}
    //   className={classNames('block w-auto h-10', className)}
    //   alt='logo'
    // />
    <span style={{
      color: theme === 'light' ? '#000' : '#fff',
      fontSize: '20px',
      fontWeight: 'bold'
    }}>智 定 义</span>
  )
}

export default LogoSite
