# 🐛 Bug Tracker & Fix Priority

## CRITICAL BUGS (Fix Immediately)

### Bug #1: Bare Exception Handling
**Location:** `core/memory.py:550-552`
**Severity:** 🔴 CRITICAL
**Description:** Silently swallows all exceptions
```python
try:
    data = json.load(f)
except Exception:  # ❌ This hides everything!
    return
```
**Impact:** Data corruption goes unnoticed
**Fix Time:** 30 minutes
**Status:** ⏳ PENDING

---

### Bug #2: asyncio.run() in Thread
**Location:** `main.py:71`
**Severity:** 🔴 CRITICAL
**Description:** Creates new event loop each call - thread unsafe
```python
threading.Thread(target=lambda: asyncio.run(self.run_ai(user_text))).start()
```
**Impact:** Random crashes, race conditions
**Fix Time:** 40 minutes
**Status:** ⏳ PENDING

---

### Bug #3: Memory Leak in Sessions
**Location:** `voice/dialogue.py:354-363`
**Severity:** 🔴 CRITICAL
**Description:** Old dialogue sessions never cleaned up
```python
def reset_session(self):
    self.session = DialogueSession()  # Old session lost?
```
**Impact:** Memory grows indefinitely
**Fix Time:** 20 minutes
**Status:** ⏳ PENDING

---

### Bug #4: PIL Resource Leak
**Location:** `automation/ocr_control.py:100-154`
**Severity:** 🔴 CRITICAL
**Description:** Image objects not closed after use
```python
def screenshot(self):
    image = ImageGrab.grab()  # Never closed!
    return image
```
**Impact:** Memory bloat over time
**Fix Time:** 15 minutes
**Status:** ⏳ PENDING

---

### Bug #5: Disk I/O Bottleneck
**Location:** `core/memory.py:457-524`
**Severity:** 🔴 CRITICAL
**Description:** Every operation writes to disk
```python
if self.auto_save:
    self.save()  # Called on every add_conversation!
```
**Impact:** 10x slower than necessary
**Fix Time:** 30 minutes
**Status:** ⏳ PENDING

---

## HIGH SEVERITY BUGS

### Bug #6: O(n) Search Complexity
**Location:** `voice/dialogue.py:254-266`
**Severity:** 🟠 HIGH
**Description:** Linear search for last message
```python
def last_user_message(self):
    for message in reversed(self.session.messages):  # O(n)!
        if message.role == "user":
            return message
```
**Impact:** Slow with large conversations
**Fix Time:** 15 minutes
**Status:** ⏳ PENDING

---

### Bug #7: Thread Safety Missing
**Location:** `voice/dialogue.py` (multiple methods)
**Severity:** 🟠 HIGH
**Description:** No locks on shared data
```python
def last_user_message(self):
    for message in reversed(self.session.messages):  # Race condition!
        if message.role == "user":
            return message
```
**Impact:** Data corruption under concurrent access
**Fix Time:** 1 hour
**Status:** ⏳ PENDING

---

### Bug #8: No OCR Caching
**Location:** `automation/ocr_control.py:370-415`
**Severity:** 🟠 HIGH
**Description:** Same screen OCR'd multiple times
```python
def find_text_position(self, keyword):
    image = self.screenshot()  # Full screen grab
    data = pytesseract.image_to_data(image)  # Full OCR every time!
```
**Impact:** 5x slower than necessary
**Fix Time:** 20 minutes
**Status:** ⏳ PENDING

---

### Bug #9: Incomplete Async Implementation
**Location:** `main.py:40-46`
**Severity:** 🟠 HIGH
**Description:** TTS blocking, should be async
```python
async def speak(self, text):
    comm = Communicate(text=text, voice="bn-BD-NabanitaNeural")
    await comm.save("response.mp3")  # But then:
    os.system("start response.mp3")  # Blocks here!
```
**Impact:** UI freezes during playback
**Fix Time:** 30 minutes
**Status:** ⏳ PENDING

---

### Bug #10: Duplicate Files
**Location:** `core/memory.py` vs `ai/memory.py`
**Severity:** 🟠 HIGH
**Description:** Same module in two places
```
core/memory.py       415 lines (full)
ai/memory.py         61 lines (partial?)
```
**Impact:** Maintenance nightmare, confusion
**Fix Time:** 1 hour
**Status:** ⏳ PENDING

---

## MEDIUM SEVERITY BUGS

### Bug #11: Empty Stub Plugins
**Location:** `plugins/*.py`
**Severity:** 🟡 MEDIUM
**Description:** 59 files with 0 lines
```python
# deepseek_plugin.py (3 lines)
# Only imports, no implementation!
```
**Impact:** Dead code, confusing
**Fix Time:** 8 hours (implementation)
**Status:** ⏳ PENDING

---

### Bug #12: No Error Propagation
**Location:** Multiple modules
**Severity:** 🟡 MEDIUM
**Description:** Errors logged but not raised
```python
except Exception:
    logger.exception("OCR Failed")  # Logged but...
    return None  # Caller doesn't know it failed!
```
**Impact:** Silent failures, debugging hard
**Fix Time:** 2 hours
**Status:** ⏳ PENDING

---

### Bug #13: Poor Test Coverage
**Location:** All modules
**Severity:** 🟡 MEDIUM
**Description:** Only 6% coverage
**Impact:** Regressions go unnoticed
**Fix Time:** 20 hours
**Status:** ⏳ PENDING

---

### Bug #14: Missing Documentation
**Location:** All modules
**Severity:** 🟡 MEDIUM
**Description:** No docstrings in most functions
**Impact:** Hard to maintain
**Fix Time:** 10 hours
**Status:** ⏳ PENDING

---

## FIX PLAN

### Phase 1: Critical Fixes (Day 1)
```
Bug #1: Exception handling        30 min
Bug #2: asyncio.run() loop        40 min
Bug #4: PIL resource leak         15 min
Bug #5: Disk I/O batching         30 min
────────────────────────────────
Total: 1 hour 55 min
```

### Phase 2: High Priority (Day 2)
```
Bug #6: O(n) → O(1) search        15 min
Bug #7: Add thread locks           1 hour
Bug #8: OCR caching                20 min
Bug #9: Async TTS                  30 min
Bug #10: Fix duplicate files       1 hour
────────────────────────────────
Total: 3 hours 35 min
```

### Phase 3: Medium Priority (Week 1)
```
Bug #11: Complete stub plugins    8 hours
Bug #12: Error propagation         2 hours
Bug #13: Increase test coverage   20 hours
Bug #14: Add documentation        10 hours
────────────────────────────────
Total: 40 hours
```

---

## TESTING CHECKLIST

- [ ] Run memory save test (check disk writes)
- [ ] Run dialogue test with 1000 messages
- [ ] Run OCR test (measure performance)
- [ ] Run async test (check for race conditions)
- [ ] Run long-running app test (24 hours)
- [ ] Memory usage profiling
- [ ] Thread safety test
- [ ] All unit tests pass
