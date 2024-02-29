# Blender for UniHSI

## Save motion sequence
```
def __init__():
    self.output_dict['trans'] = np.zeros([self.record_frame_number, 15, 3])
    self.output_dict['rot'] = np.zeros([self.record_frame_number, 15, 4])

def _compute_task_obs():
    if self.record_step < self.record_frame_number:
        self.output_dict['trans'][self.record_step] = self._rigid_body_pos[0].cpu().numpy()
        self.output_dict['rot'][self.record_step] = self._rigid_body_rot[0].cpu().numpy()
    if self.record_step == self.record_frame_number:
        np.save("motion_sequence/motion_simple_sit.npy", self.output_dict)
    self.record_step += 1
    print(self.record_step)
```

## Transfer motion sequence to mesh
config and run motionseq2mesh.py

## Run blender

### Run it in commands
```
path_to_blender/blender
```

### Click "Scripting" in the upper menu

### Open python file
e.g. demo_multistep_multiobj_2.py

### Click "Run Script"

