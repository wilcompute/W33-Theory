"""Reject valid Wasm programs outside the sparse compiler's exact witness."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
import w33_dynamic_sparse_memory_counter as sparse


class SparseCompilerAdmissionTests(unittest.TestCase):
    def test_original_source_and_counter_agree_for_every_admitted_address(self):
        module = sparse.cap.decode_module(sparse.build_dynamic_module())
        compiler = sparse.SparseCompiler(module)
        program, _ = compiler.compile()
        for address in sparse.ALLOWED:
            with self.subTest(address=address):
                runtime = sparse.cap.CapabilityWasmRuntime(
                    module, host_functions={("w33.kernel", "ADDR"): lambda args, rt: address})
                source = runtime.execute_export("main")
                regs, _ = sparse.run_mc_initial(program, tuple(compiler.names), {"host.ADDR": address})
                self.assertEqual(source, regs[program.result_register])
                self.assertEqual(source, 77)
                for word, register in compiler.memory_regs.items():
                    self.assertEqual(runtime.load_i32(word), regs[register])
        regs, _ = sparse.run_mc_initial(program, tuple(compiler.names), {"host.ADDR": 16})
        self.assertEqual(regs[compiler.trap], 1)

    def test_same_opcodes_different_semantics_are_rejected(self):
        raw = sparse.build_dynamic_module()
        mutations = (
            (b"\x41" + sparse.cap.sleb32(77), b"\x41" + sparse.cap.sleb32(78)),
            (b"\x36\x02\x00", b"\x36\x02\x04"),
            (b"\x28\x02\x00", b"\x28\x02\x04"),
            (b"ADDR", b"ELSE"),
            (b"main", b"side"),
        )
        original_ops = [i.op for i in sparse.cap.decode_module(raw).functions[0].instructions]
        for old, new in mutations:
            with self.subTest(old=old, new=new):
                self.assertEqual(raw.count(old), 1)
                module = sparse.cap.decode_module(raw.replace(old, new))
                self.assertTrue(sparse.cap.validate(module)["valid"])
                self.assertEqual([i.op for i in module.functions[0].instructions], original_ops)
                if new == b"\x41" + sparse.cap.sleb32(78):
                    runtime = sparse.cap.CapabilityWasmRuntime(
                        module, host_functions={("w33.kernel", "ADDR"): lambda args, rt: 0})
                    self.assertEqual(runtime.execute_export("main"), 78)
                with self.assertRaisesRegex(ValueError, "unsupported sparse witness semantics"):
                    sparse.SparseCompiler(module).compile()

    def test_custom_section_changes_identity_but_preserves_supported_semantics(self):
        raw = sparse.build_dynamic_module()
        annotated = raw + sparse.cap._section(0, sparse.cap._name("audit") + b"annotation")
        module = sparse.cap.decode_module(annotated)
        self.assertNotEqual(module.binary_digest, sparse.cap.decode_module(raw).binary_digest)
        compiler = sparse.SparseCompiler(module)
        program, manifest = compiler.compile()
        regs, _ = sparse.run_mc_initial(program, tuple(compiler.names), {"host.ADDR": 4})
        self.assertEqual(regs[program.result_register], 77)
        self.assertEqual(manifest["source_binary_digest"], module.binary_digest)


if __name__ == "__main__":
    unittest.main()
