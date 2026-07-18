"""
STEP 3: INTEGRATION TEST SUITE
Test all fixed modules working together
"""

import unittest
import time
import threading
import asyncio
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================
# TEST 1: Memory Module Integration
# ============================================================

class TestMemoryModule(unittest.TestCase):
    """Test fixed memory module"""
    
    def setUp(self):
        """Setup test database"""
        from core.memory_fixed import MemoryManager
        self.memory = MemoryManager("database/test_memory.json")
    
    def tearDown(self):
        """Cleanup"""
        import shutil
        db_path = Path("database/test_memory.json")
        if db_path.exists():
            db_path.unlink()
    
    def test_batched_save(self):
        """Test batched save system"""
        print("\n[TEST] Memory batched save...")
        
        start_time = time.time()
        
        # Add 100 items
        for i in range(100):
            self.memory.remember(f"key_{i}", f"value_{i}")
        
        # Should be instant (not waiting for disk)
        elapsed = time.time() - start_time
        
        self.assertLess(elapsed, 1.0, "Should be fast without blocking")
        print(f"✅ Added 100 items in {elapsed:.2f}s")
    
    def test_proper_exception_handling(self):
        """Test exception handling"""
        print("\n[TEST] Memory exception handling...")
        
        # Test FileNotFoundError
        from core.memory_fixed import MemoryManager
        memory = MemoryManager("nonexistent/path/memory.json")
        
        try:
            memory._load()
            print("✅ FileNotFoundError handled gracefully")
        except Exception as e:
            self.fail(f"Should handle missing file: {e}")
    
    def test_thread_safety(self):
        """Test thread-safe operations"""
        print("\n[TEST] Memory thread safety...")
        
        def add_items(start, count):
            for i in range(start, start + count):
                self.memory.remember(f"key_{i}", f"value_{i}")
        
        threads = []
        for i in range(5):
            t = threading.Thread(target=add_items, args=(i*20, 20))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        # Check all items saved
        stats = self.memory.statistics()
        self.assertEqual(stats['memory_items'], 100)
        print(f"✅ Thread-safe: Added 100 items across 5 threads")

# ============================================================
# TEST 2: OCR Module Integration
# ============================================================

class TestOCRModule(unittest.TestCase):
    """Test fixed OCR module"""
    
    def setUp(self):
        """Setup OCR controller"""
        from automation.ocr_control_fixed import OCRController
        self.ocr = OCRController()
    
    def test_caching_system(self):
        """Test OCR caching"""
        print("\n[TEST] OCR caching system...")
        
        cache_stats_before = self.ocr.get_cache_stats()
        self.assertEqual(cache_stats_before['cached_results'], 0)
        
        # Cache a result manually
        self.ocr._cache_result("test:None", {"text": "Test", "confidence": 95})
        
        cache_stats_after = self.ocr.get_cache_stats()
        self.assertEqual(cache_stats_after['cached_results'], 1)
        print("✅ Caching system working")
    
    def test_cache_size_limit(self):
        """Test cache size limit"""
        print("\n[TEST] Cache size limiting...")
        
        # Fill cache beyond max
        for i in range(150):
            self.ocr._cache_result(f"key_{i}", {"text": f"Text{i}"})
        
        cache_stats = self.ocr.get_cache_stats()
        self.assertLessEqual(
            cache_stats['cached_results'],
            self.ocr._cache_max_size
        )
        print(f"✅ Cache size limited to {cache_stats['cached_results']}")
    
    def test_cache_clearing(self):
        """Test cache clearing"""
        print("\n[TEST] Cache clearing...")
        
        # Add to cache
        self.ocr._cache_result("test:None", {"text": "Test"})
        
        # Clear cache
        self.ocr.clear_ocr_cache()
        
        cache_stats = self.ocr.get_cache_stats()
        self.assertEqual(cache_stats['cached_results'], 0)
        print("✅ Cache cleared successfully")

# ============================================================
# TEST 3: Dialogue Module Integration
# ============================================================

class TestDialogueModule(unittest.TestCase):
    """Test fixed dialogue module"""
    
    def setUp(self):
        """Setup dialogue manager"""
        from voice.dialogue_fixed import ConversationManager
        self.dialogue = ConversationManager()
    
    def test_o1_lookup(self):
        """Test O(1) last message lookup"""
        print("\n[TEST] Dialogue O(1) lookup...")
        
        # Add messages
        for i in range(1000):
            if i % 2 == 0:
                self.dialogue.add_message("user", f"User msg {i}")
            else:
                self.dialogue.add_message("assistant", f"Assistant msg {i}")
        
        # Time last message lookup
        start_time = time.time()
        for _ in range(100):
            msg = self.dialogue.last_user_message()
        elapsed = time.time() - start_time
        
        # Should be very fast (< 1ms per call)
        avg_time = (elapsed / 100) * 1000  # milliseconds
        self.assertLess(avg_time, 1.0, "Should be O(1) - sub-millisecond")
        print(f"✅ O(1) lookup: {avg_time:.3f}ms per call")
    
    def test_thread_safety(self):
        """Test thread-safe operations"""
        print("\n[TEST] Dialogue thread safety...")
        
        def add_messages(role, count):
            for i in range(count):
                self.dialogue.add_message(role, f"{role} message {i}")
        
        threads = [
            threading.Thread(target=add_messages, args=("user", 50)),
            threading.Thread(target=add_messages, args=("assistant", 50)),
        ]
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        
        stats = self.dialogue.statistics()
        self.assertEqual(stats['messages'], 100)
        print(f"✅ Thread-safe: {stats['messages']} messages added")
    
    def test_session_archive(self):
        """Test session archiving"""
        print("\n[TEST] Session archiving...")
        
        # Add messages
        for i in range(10):
            self.dialogue.add_message("user", f"Msg {i}")
        
        # Reset session
        self.dialogue.reset_session()
        
        # Check archive
        history = self.dialogue.get_session_history()
        self.assertEqual(len(history), 1)
        print("✅ Session archived successfully")
    
    def test_pointer_update_on_delete(self):
        """Test pointer update when deleting"""
        print("\n[TEST] Pointer update on delete...")
        
        self.dialogue.add_message("user", "Msg 1")
        self.dialogue.add_message("user", "Msg 2")
        
        # Remove last
        self.dialogue.remove_last_message()
        
        # Check pointer still valid
        msg = self.dialogue.last_user_message()
        self.assertIsNotNone(msg)
        self.assertEqual(msg.content, "Msg 1")
        print("✅ Pointer updated correctly on delete")

# ============================================================
# TEST 4: Event Loop Integration
# ============================================================

class TestEventLoop(unittest.TestCase):
    """Test event loop implementation"""
    
    def test_global_event_loop(self):
        """Test global event loop creation"""
        print("\n[TEST] Global event loop...")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        results = []
        
        async def task(i):
            await asyncio.sleep(0.01)
            return i
        
        # Schedule 100 coroutines
        futures = []
        for i in range(100):
            future = asyncio.run_coroutine_threadsafe(task(i), loop)
            futures.append(future)
        
        # Wait for all
        for future in futures:
            try:
                result = future.result(timeout=5)
                results.append(result)
            except Exception as e:
                self.fail(f"Task failed: {e}")
        
        loop.call_soon_threadsafe(loop.stop)
        
        self.assertEqual(len(results), 100)
        print(f"✅ Event loop: {len(results)} tasks completed")
    
    def test_multiple_coroutines(self):
        """Test multiple concurrent coroutines"""
        print("\n[TEST] Multiple concurrent coroutines...")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def dummy_task(duration):
            await asyncio.sleep(duration)
            return True
        
        # Run 50 concurrent tasks
        futures = []
        for i in range(50):
            future = asyncio.run_coroutine_threadsafe(
                dummy_task(0.1),
                loop
            )
            futures.append(future)
        
        # Wait for all
        success_count = 0
        for future in futures:
            try:
                if future.result(timeout=5):
                    success_count += 1
            except Exception as e:
                pass
        
        loop.call_soon_threadsafe(loop.stop)
        
        self.assertEqual(success_count, 50)
        print(f"✅ Concurrent tasks: {success_count}/50 successful")

# ============================================================
# TEST 5: Integration Test (All modules together)
# ============================================================

class TestIntegration(unittest.TestCase):
    """Test all modules working together"""
    
    def setUp(self):
        """Setup all modules"""
        from core.memory_fixed import MemoryManager
        from automation.ocr_control_fixed import OCRController
        from voice.dialogue_fixed import ConversationManager
        
        self.memory = MemoryManager("database/integration_test.json")
        self.ocr = OCRController()
        self.dialogue = ConversationManager()
    
    def tearDown(self):
        """Cleanup"""
        import shutil
        db_path = Path("database/integration_test.json")
        if db_path.exists():
            db_path.unlink()
    
    def test_workflow(self):
        """Test complete workflow"""
        print("\n[TEST] Complete workflow integration...")
        
        # 1. Add conversation to memory
        self.memory.add_conversation("user", "Hello")
        
        # 2. Add to dialogue
        self.dialogue.add_message("user", "Hello")
        
        # 3. Add response to dialogue
        self.dialogue.add_message("assistant", "Hi there!")
        
        # 4. Save response to memory
        self.memory.add_conversation("assistant", "Hi there!")
        
        # 5. Verify all saved
        conv_stats = self.memory.statistics()
        dial_stats = self.dialogue.statistics()
        
        self.assertEqual(conv_stats['conversation'], 2)
        self.assertEqual(dial_stats['messages'], 2)
        
        print("✅ Complete workflow successful")
    
    def test_performance_under_load(self):
        """Test performance with heavy load"""
        print("\n[TEST] Performance under load...")
        
        start_time = time.time()
        
        # Simulate busy system
        for i in range(100):
            self.memory.remember(f"item_{i}", f"value_{i}")
            self.dialogue.add_message(
                "user" if i % 2 == 0 else "assistant",
                f"Message {i}"
            )
        
        elapsed = time.time() - start_time
        
        # Should still be responsive
        self.assertLess(elapsed, 5.0, "Should handle load efficiently")
        print(f"✅ Processed 100 items + messages in {elapsed:.2f}s")
    
    def test_concurrent_access(self):
        """Test concurrent access to all modules"""
        print("\n[TEST] Concurrent access...")
        
        def worker(thread_id):
            for i in range(20):
                # Memory
                self.memory.remember(f"t{thread_id}_k{i}", f"value{i}")
                
                # Dialogue
                self.dialogue.add_message(
                    "user",
                    f"Thread {thread_id} message {i}"
                )
        
        threads = []
        for i in range(5):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        stats = self.memory.statistics()
        dial_stats = self.dialogue.statistics()
        
        self.assertEqual(stats['memory_items'], 100)
        self.assertEqual(dial_stats['messages'], 100)
        print("✅ Concurrent access: 5 threads × 20 items each = 100 items")

# ============================================================
# RUN ALL TESTS
# ============================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("STEP 3: INTEGRATION TEST SUITE")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all tests
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryModule))
    suite.addTests(loader.loadTestsFromTestCase(TestOCRModule))
    suite.addTests(loader.loadTestsFromTestCase(TestDialogueModule))
    suite.addTests(loader.loadTestsFromTestCase(TestEventLoop))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
        print("🎉 All fixed modules are working correctly!")
    else:
        print("\n❌ SOME TESTS FAILED")
        print("Review the errors above and fix accordingly")
    
    print("="*70 + "\n")
