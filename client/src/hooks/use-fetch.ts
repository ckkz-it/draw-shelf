import { useCallback, useEffect, useState } from 'react';

type useFetchState<T = any> = { result: T; error: any; loading: boolean; fetched: boolean };

export const useFetch = <T>(fetchFn: (...args: any) => Promise<T>, immediate = true) => {
  const [state, setState] = useState<useFetchState<T>>({
    result: null,
    error: null,
    loading: false,
    fetched: false,
  });

  const fetchRequest = useCallback(async () => {
    setState((s) => ({ ...s, loading: true }));
    try {
      const data = await fetchFn();
      if (data !== undefined) {
        setState((s) => ({ ...s, result: data }));
      }
    } catch (err) {
      setState((s) => ({ ...s, error: err }));
    } finally {
      setState((s) => ({ ...s, fetched: true, loading: false }));
    }
  }, [fetchFn]);

  const makeRequest = () => fetchRequest();

  useEffect(() => {
    if (!state.fetched && immediate) {
      fetchRequest();
    }
  }, [state.fetched, fetchRequest, immediate]);

  return { ...state, makeRequest };
};
