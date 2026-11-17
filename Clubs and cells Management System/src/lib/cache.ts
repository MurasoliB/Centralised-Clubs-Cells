// Bounded LRU In-Memory Cache with Zero Memory-Leak Architecture + Session Storage Persistence
interface CacheEntry<T> {
  data: T;
  timestamp: number;
}

const MAX_CACHE_ENTRIES = 35;
const memoryStore = new Map<string, CacheEntry<any>>();

export const cache = {
  /**
   * Retrieve cached data if present and not expired (default TTL: 5 minutes)
   */
  get<T>(key: string, maxAgeMs = 300000): T | null {
    // 1. Check in-memory LRU cache
    const entry = memoryStore.get(key);
    if (entry) {
      if (Date.now() - entry.timestamp > maxAgeMs) {
        memoryStore.delete(key);
        try {
          sessionStorage.removeItem(`kec_cache_${key}`);
        } catch {}
        return null;
      }
      // Move key to the end of the map to maintain LRU order
      memoryStore.delete(key);
      memoryStore.set(key, entry);
      return entry.data as T;
    }

    // 2. Check sessionStorage fallback (instant restore across page transitions)
    try {
      const raw = sessionStorage.getItem(`kec_cache_${key}`);
      if (raw) {
        const stored = JSON.parse(raw) as CacheEntry<T>;
        if (Date.now() - stored.timestamp <= maxAgeMs) {
          memoryStore.set(key, stored);
          return stored.data;
        } else {
          sessionStorage.removeItem(`kec_cache_${key}`);
        }
      }
    } catch {}

    return null;
  },

  /**
   * Store data in bounded memory cache + sessionStorage (auto-evicts oldest entries to prevent RAM bloating)
   */
  set<T>(key: string, data: T): void {
    const entry: CacheEntry<T> = {
      data,
      timestamp: Date.now(),
    };

    if (memoryStore.has(key)) {
      memoryStore.delete(key);
    } else if (memoryStore.size >= MAX_CACHE_ENTRIES) {
      // Evict oldest (first inserted) item to strictly enforce bounded memory
      const oldestKey = memoryStore.keys().next().value;
      if (oldestKey) {
        memoryStore.delete(oldestKey);
      }
    }

    memoryStore.set(key, entry);

    try {
      sessionStorage.setItem(`kec_cache_${key}`, JSON.stringify(entry));
    } catch {}
  },

  /**
   * Check if a valid non-expired cache entry exists
   */
  has(key: string, maxAgeMs = 300000): boolean {
    return cache.get(key, maxAgeMs) !== null;
  },

  /**
   * Invalidate specific keys or keys matching a prefix
   */
  invalidate(keyPrefix?: string): void {
    if (!keyPrefix) {
      memoryStore.clear();
      try {
        const keysToRemove: string[] = [];
        for (let i = 0; i < sessionStorage.length; i++) {
          const k = sessionStorage.key(i);
          if (k && k.startsWith('kec_cache_')) {
            keysToRemove.push(k);
          }
        }
        keysToRemove.forEach((k) => sessionStorage.removeItem(k));
      } catch {}
      return;
    }

    const keysToDelete: string[] = [];
    for (const key of memoryStore.keys()) {
      if (key.startsWith(keyPrefix)) {
        keysToDelete.push(key);
      }
    }
    for (const k of keysToDelete) {
      memoryStore.delete(k);
      try {
        sessionStorage.removeItem(`kec_cache_${k}`);
      } catch {}
    }
  },
};

