'use client'
import type { FC } from 'react'
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

  return (
    <span style={{ fontWeight: 700, fontSize: '20px' }}>智 定 义</span>
  )
}

export default LogoSite
