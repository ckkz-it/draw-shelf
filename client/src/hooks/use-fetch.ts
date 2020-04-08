import { useEffect, useState } from 'react';

type useFetchState<T = any> = { result: T; error: any; loading: boolean; fetched: boolean };

export const useFetch = <T>(fetchFn: (...args: any) => Promise<T>) => {
  const [state, setState] = useState<useFetchState<T>>({
    result: null,
    error: null,
    loading: null,
    fetched: null,
  });

  useEffect(() => {
    if (!state.loading && !state.fetched) {
      setState((s) => ({ ...s, loading: true }));
      fetchFn()
        .then((resp) => {
          if (resp !== undefined) {
            setState((s) => ({ ...s, result: resp }));
          }
        })
        .catch((error: any) => {
          setState((s) => ({ ...s, error }));
        })
        .finally(() => {
          setState((s) => ({ ...s, fetched: true, loading: false }));
        });
    }
  }, [state, fetchFn]);

  return state;
};
