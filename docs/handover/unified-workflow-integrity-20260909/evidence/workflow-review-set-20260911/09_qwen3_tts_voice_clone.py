# vibecomfy: generated
# For hand-editing, run: python -m vibecomfy.cli copy-to-recipe <id>
# vibecomfy: surface=canonical
"""Auto-generated ready_template — use python -m vibecomfy.cli copy-to-recipe <id> for hand-editing."""
from __future__ import annotations

from vibecomfy.templates import InputSpec, ReadyMetadata, authored_channel, new_workflow, ref
from vibecomfy.workflow import VibeWorkflow
from vibecomfy.nodes.core import LoadAudio, SaveAudioMP3
from vibecomfy.nodes.qwentts import AILab_Qwen3TTSVoiceClone


DEFAULT_SEED = 125
SPEECH_SMOKE_WAV = 'speech_smoke.wav'


PUBLIC_INPUT_METADATA = {
    'seed': InputSpec(node=ref('ailab_qwen3ttsvoiceclone'), field='seed', default=None, infer_type=False),
}

CANONICAL_CUSTODY = {'loadaudio': {'id': '1',
               'uid': '1',
               'class_type': 'LoadAudio',
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
                            'provenance': 'untrusted_source',
                            'output_names': ['AUDIO'],
                            'output_types': ['AUDIO']},
               'widget_channels': {'audio': 'widget_0'},
               'none_input_fields': [],
               'none_widget_fields': [],
               'output_slot_names': {},
               'construction_output_names': ['AUDIO']},
 'ailab_qwen3ttsvoiceclone': {'id': '2',
                              'uid': '2',
                              'class_type': 'AILab_Qwen3TTSVoiceClone',
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
 'saveaudiomp3': {'id': '3',
                  'uid': '3',
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
    template_id='qwen3_tts_voice_clone',
    inputs=PUBLIC_INPUT_METADATA,
    custom_node_packs={'ComfyUI-QwenTTS': {'commit': 'd8122a8ba835b65fd65c113d2b273b1ad1579293', 'url': 'https://github.com/1038lab/ComfyUI-QwenTTS.git', 'class_schema_sha256': '4137bb4f37ea178be0e794377829905d9ede1bc65496a23a51d766a3f03b2c84', 'classes_used': ['AILab_Qwen3TTSVoiceClone'], 'pip_packages': ['accelerate', 'librosa', 'openai-whisper', 'qwen-tts', 'soundfile', 'tiktoken'], 'status': 'discovered'}},
    provenance={'source_path': 'ready_templates/sources/custom_nodes/qwen_tts/1038lab/qwen3_tts_voice_clone.json', 'source_id': 'qwen3_tts_voice_clone', 'source_type': 'api', 'source_workflow_path': 'ready_templates/sources/custom_nodes/qwen_tts/1038lab/qwen3_tts_voice_clone.json', 'source_ref': 'ready_templates/sources/custom_nodes/qwen_tts/1038lab/qwen3_tts_voice_clone.json', 'source_kind': 'raw_json', 'indexed_id': None, 'workflow_source_id': 'qwen3_tts_voice_clone', 'workflow_source_type': 'api', 'raw_workflow_shape': 'api', 'source_hash': 'sha256:e3ce2d13899343e5431b0c474af98f58beac18240668c448da9565aa62484cc6', 'workflow_shape': {'nodes': 3, 'runtime_nodes': 3, 'helper_nodes': 0, 'edges': 2, 'inputs': 1, 'outputs': 1}, 'output_mode': 'scratchpad'},
)

def build() -> VibeWorkflow:
    """Build the workflow (auto-generated)."""
    wf = new_workflow(READY_METADATA, source_path=__file__, canonical_custody=CANONICAL_CUSTODY)

    loadaudio = LoadAudio(
        audio=authored_channel(SPEECH_SMOKE_WAV, widget='speech_smoke.wav', name='widget_0'),
    )

    ailab_qwen3ttsvoiceclone = AILab_Qwen3TTSVoiceClone(
        target_text='This Qwen voice clone template uses a tiny bundled reference clip and runs as a reusable audio smoke test.',
        model_size='0.6B',
        language='English',
        reference_text='This is a short reference audio sample for workflow smoke testing.',
        x_vector_only=False,
        unload_models=True,
        seed=DEFAULT_SEED,
        reference_audio=loadaudio.out('AUDIO'),
    )

    saveaudiomp3 = SaveAudioMP3(
        filename_prefix='audio/qwen3_tts_voice_clone',
        quality='V0',
        audio=ailab_qwen3ttsvoiceclone.out('audio'),
    )

    wf = wf.finalize(PUBLIC_INPUT_METADATA, canonical_outputs=[{'node': saveaudiomp3, 'output_type': 'SaveAudioMP3', 'name': None, 'artifact_kind': None, 'mime_type': None, 'filename_prefix': None, 'expected_cardinality': None}], canonical_requirements={'models': [], 'custom_nodes': [], 'missing_models': [], 'missing_nodes': [], 'unsupported': []}, canonical_custody=CANONICAL_CUSTODY, canonical_bindings={'loadaudio': loadaudio, 'ailab_qwen3ttsvoiceclone': ailab_qwen3ttsvoiceclone, 'saveaudiomp3': saveaudiomp3})
    wf.strict_types = False
    return wf
