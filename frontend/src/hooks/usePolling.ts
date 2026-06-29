import { useState, useEffect, useRef, useCallback } from 'react'

interface UsePollingOptions {
  interval?: number
  enabled?: boolean
  maxAttempts?: number
}

interface UsePollingResult<T> {
  data: T | null
  loading: boolean
  error: Error | null
  stop: () => void
  restart: () => void
}

export function usePolling<T>(
  fetchFunction: () => Promise<T>,
  options: UsePollingOptions = {}
): UsePollingResult<T> {
  const {
    interval = 2000,
    enabled = true,
    maxAttempts = Infinity
  } = options
  
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)
  const [isRunning, setIsRunning] = useState(enabled)
  
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const attemptsRef = useRef(0)
  
  const stop = useCallback(() => {
    setIsRunning(false)
    if (timerRef.current) {
      clearTimeout(timerRef.current)
      timerRef.current = null
    }
  }, [])
  
  const restart = useCallback(() => {
    attemptsRef.current = 0
    setIsRunning(true)
  }, [])
  
  useEffect(() => {
    if (!isRunning) return
    
    const poll = async () => {
      setLoading(true)
      setError(null)
      
      try {
        const result = await fetchFunction()
        setData(result)
        attemptsRef.current += 1
        
        if (attemptsRef.current >= maxAttempts) {
          stop()
        }
      } catch (err) {
        const error = err instanceof Error ? err : new Error(String(err))
        setError(error)
      } finally {
        setLoading(false)
      }
    }
    
    // 立即执行一次
    poll()
    
    // 设置定时器
    timerRef.current = setInterval(poll, interval)
    
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current)
      }
    }
  }, [isRunning, fetchFunction, interval, maxAttempts, stop])
  
  return { data, loading, error, stop, restart }
}
