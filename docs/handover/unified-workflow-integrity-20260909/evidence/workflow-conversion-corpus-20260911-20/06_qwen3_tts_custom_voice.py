# vibecomfy: generated
# For hand-editing, run: python -m vibecomfy.cli copy-to-recipe <id>
# vibecomfy: surface=canonical
"""Auto-generated ready_template — use python -m vibecomfy.cli copy-to-recipe <id> for hand-editing."""
from __future__ import annotations

from vibecomfy.templates import InputSpec, ReadyMetadata, new_workflow, ref
from vibecomfy.workflow import VibeWorkflow
from vibecomfy.nodes.core import SaveAudioMP3
from vibecomfy.nodes.qwentts import AILab_Qwen3TTSCustomVoice


DEFAULT_PROMPT = 'VibeComfy generated this short Qwen voice smoke test from a reusable Python template.'
DEFAULT_SEED = 123


PUBLIC_INPUT_METADATA = {
    'seed': InputSpec(node=ref('ailab_qwen3ttscustomvoice'), field='seed', default=None, infer_type=False),
}

CANONICAL_CUSTODY = {'ailab_qwen3ttscustomvoice': {'id': '1',
                               'uid': '1',
                               'class_type': 'AILab_Qwen3TTSCustomVoice',
                               'native_ports': {'native_input_names': None,
                                                'native_output_names': None,
                                                'native_input_types': None,
                                                'native_output_types': None,
                                                'native_input_optional': None,
                                                'native_input_asset_kinds': None,
                                                'native_output_slots': None},
                               'metadata': {'schema_source': {'provider': 'object_info_index',
                                                              'path': None,
                                                              'cache_path': '/Users/hannahomalley/Documents/Codex/2026-09-08/goal-continue-the-existing-megado-plan/VibeComfy-integrity/.otto/worktrees/unified-workflow-integrity-20260909/vibecomfy/porting/cache/object_info/AILab_QwenTTS@runpod-snapshot.json',
                                                              'server_url': None,
                                                              'package': 'AILab_QwenTTS',
                                                              'version': None,
                                                              'hash': None,
                                                              'confidence': 0.7},
                                            'provenance': 'untrusted_source',
                                            'output_names': ['audio'],
                                            'output_types': ['AUDIO']},
                               'widget_channels': {},
                               'none_input_fields': [],
                               'none_widget_fields': [],
                               'output_slot_names': {},
                               'construction_output_names': ['audio']},
 'saveaudiomp3': {'id': '2',
                  'uid': '2',
                  'class_type': 'SaveAudioMP3',
                  'native_ports': {'native_input_names': None,
                                   'native_output_names': None,
                                   'native_input_types': None,
                                   'native_output_types': None,
                                   'native_input_optional': None,
                                   'native_input_asset_kinds': None,
                                   'native_output_slots': None},
                  'metadata': {'schema_source': {'provider': 'object_info_index',
                                                 'path': None,
                                                 'cache_path': '/Users/hannahomalley/Documents/Codex/2026-09-08/goal-continue-the-existing-megado-plan/VibeComfy-integrity/.otto/worktrees/unified-workflow-integrity-20260909/vibecomfy/porting/cache/object_info/comfy_core@object_info_comfyui_0.24.0.1.json',
                                                 'server_url': None,
                                                 'package': 'comfy_core',
                                                 'version': None,
                                                 'hash': None,
                                                 'confidence': 0.7},
                               'provenance': 'untrusted_source'},
                  'widget_channels': {},
                  'none_input_fields': [],
                  'none_widget_fields': [],
                  'output_slot_names': {}}}

READY_METADATA = ReadyMetadata.build(
    capability='audio',
    template_id='qwen3_tts_custom_voice',
    inputs=PUBLIC_INPUT_METADATA,
    custom_node_packs={'ComfyUI-QwenTTS': {'commit': 'd8122a8ba835b65fd65c113d2b273b1ad1579293', 'url': 'https://github.com/1038lab/ComfyUI-QwenTTS.git', 'class_schema_sha256': '4137bb4f37ea178be0e794377829905d9ede1bc65496a23a51d766a3f03b2c84', 'classes_used': ['AILab_Qwen3TTSCustomVoice'], 'pip_packages': ['accelerate', 'librosa', 'openai-whisper', 'qwen-tts', 'soundfile', 'tiktoken'], 'status': 'discovered'}},
    provenance={'source_path': 'ready_templates/sources/custom_nodes/qwen_tts/1038lab/qwen3_tts_custom_voice.json', 'source_id': 'qwen3_tts_custom_voice', 'source_type': 'api', 'source_workflow_path': 'ready_templates/sources/custom_nodes/qwen_tts/1038lab/qwen3_tts_custom_voice.json', 'source_ref': 'ready_templates/sources/custom_nodes/qwen_tts/1038lab/qwen3_tts_custom_voice.json', 'source_kind': 'raw_json', 'indexed_id': None, 'workflow_source_id': 'qwen3_tts_custom_voice', 'workflow_source_type': 'api', 'raw_workflow_shape': 'api', 'source_hash': 'sha256:c6aed8da86a51e4590ae97497301e7d2cb30cbb4a8123f273ec25956c0243053', 'workflow_shape': {'nodes': 2, 'runtime_nodes': 2, 'helper_nodes': 0, 'edges': 1, 'inputs': 1, 'outputs': 1}, 'output_mode': 'scratchpad'},
)

def build() -> VibeWorkflow:
    """Build the workflow (auto-generated)."""
    wf = new_workflow(READY_METADATA, source_path=__file__, canonical_custody=CANONICAL_CUSTODY)

    ailab_qwen3ttscustomvoice = AILab_Qwen3TTSCustomVoice(
        instruct='Calm, clear, friendly delivery.',
        language='English',
        model_size='0.6B',
        seed=DEFAULT_SEED,
        speaker='Ryan',
        text=DEFAULT_PROMPT,
        unload_models=True,
    )

    saveaudiomp3 = SaveAudioMP3(
        filename_prefix='audio/qwen3_tts_custom_voice',
        quality='V0',
        audio=ailab_qwen3ttscustomvoice.out('audio'),
    )

    wf = wf.finalize(PUBLIC_INPUT_METADATA, canonical_outputs=[{'node': saveaudiomp3, 'output_type': 'SaveAudioMP3', 'name': None, 'artifact_kind': None, 'mime_type': None, 'filename_prefix': None, 'expected_cardinality': None}], canonical_requirements={'models': [], 'custom_nodes': [], 'missing_models': [], 'missing_nodes': [], 'unsupported': []}, canonical_custody=CANONICAL_CUSTODY, canonical_bindings={'ailab_qwen3ttscustomvoice': ailab_qwen3ttscustomvoice, 'saveaudiomp3': saveaudiomp3})
    wf.strict_types = False
    return wf
