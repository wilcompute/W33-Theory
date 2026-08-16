import W33.OddQRank
import W33.FourierBlocks
import W33.HeisenbergQ3
import W33.ShadowDichotomy
import W33.RankLaw
import W33.Pass441SmithPairing
import W33.Pass446CoverArray
import W33.Pass447SpanLemma
import W33.Pass450CentralFourierScaffold
import W33.Pass457PerpMonotonicity
import W33.Pass462CoverLawL1Q3
import W33.Pass465CoverLawL2L4Q3
import W33.Pass477UniformProjectiveCardinality
import W33.Pass481FirstOrderPairing
import W33.Pass484AntisymmetricVanishing
import W33.Pass486DetDivisibility
import W33.Pass487NewtonInduction
import W33.Pass488FlatBlockQuadratic
import W33.Pass491HermitianRealDet
import W33.Pass502HjelmslevGram
import W33.Pass502RelativeNormSquare
import W33.Pass508FactorialReduction
import W33.Pass511OddClassVanishing
import W33.Pass514Sieve
import W33.Pass515TriangularRank
import W33.Pass517ClosedForm
import W33.Pass533HermitianReal
import W33.Pass557ConstantValuation
import W33.Pass557OddPeriodLift
import W33.Pass560CyclotomicUniformizer
import W33.Pass565CyclotomicFiveOrder
import W33.Pass570CyclotomicResidue
import W33.Pass575CyclotomicDVRKernel
import W33.Pass581CyclotomicCompletion
import W33.Pass586CyclotomicLocalizedDVR
import W33.Pass591CyclotomicDedekindDVR
import W33.Pass806TwoBranchGluing
-- Pass828 is now imported.  It used to be excluded because
-- `gluing_order_not_perfect_square` was proved by `native_decide`, which cannot
-- work on `¬ ∃ k : ℕ, ...` -- an unbounded existential has no Decidable instance.
-- The docstring already stated the real argument (a square has even valuation at
-- every prime, and v_5 = 1 is odd), so the theorem is now proved that way from the
-- module's own `v5_gluing_order`.  Excluding it had kept the whole module
-- unchecked, not just that one line.
import W33.Pass828CoalescenceArithmetic
import W33.Pass1006RamifiedFiltration
import W33.Pass1018PencilRigidity
import W33.Pass1063SignedLiftObstruction
import W33.Pass1074SchurCocycleExtension
import W33.Pass1091FrameOrbitalIntertwiner
import W33.Pass1096CharacterHesseE8Lock
import W33.Pass1106CliffordFirewallCarrier
import W33.Pass1390FrameCrossMatching
import W33.CosineSequence
