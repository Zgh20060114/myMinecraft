#version 330 core
layout(location=0) in uvec3 in_position;
layout(location=1) in uint  in_voxel_id;
layout(location=2) in uint  in_face_id;
layout(location=3) in uint  in_ao_id;
layout(location=4) in uint  in_flip_id;

out vec2 out_uv;
out float out_position_y;
// out vec3 out_voxel_color;
out float shading;
flat out uint out_voxel_id;
flat out uint out_face_id;

uniform mat4 m_model;
uniform mat4 m_view;
uniform mat4 m_projection;

const float ao_ratio[4] = float[](0.1,0.25, 0.5,1.0);
// const float face_shading[6] = float[](1.0, 0.5, 0.5,0.8,0.5,0.8); // mc默认光照从右后方照射
const float face_shading[6] = float[](0.5, 0.5, 1.0,0.8,0.5,0.8); // mc默认光照从右后方照射

vec3 get_color(float p) {
    vec3 p3 = fract(vec3(p * 21.2) * vec3(0.1031, 0.1029, 0.0973));
    p3 += dot(p3, p3.yzx + 19.19);
    return fract((p3.xxy + p3.yzz) * p3.zyx) + 0.05;
}

const vec2 uv_coords[4] = vec2[](
    vec2(0.0, 0.0),
    vec2(1.0, 0.0),
    vec2(1.0,1.0),
    vec2(0.0, 1.0)
    );
const int uv_indices[12] = int[](3,1,0,3,2,1, 2,1,0,2,0,3);

void main(){
  gl_Position = m_projection * m_view * m_model * vec4(in_position, 1.0f);

  // out_voxel_color = get_color(in_voxel_id);
  // if (in_face_id == 0u) {
  //   // out_color = vec4(0.0f,1.0f,1.0f, 1.0f);
  //   out_color = vec3(in_voxel_id * 0.1, in_face_id * 0.1, 0.5);
  // }
  // out_color = vec4(0.6f,0.4f,0.5f, 1.0f);
  // if(in_voxel_id != 0u && in_face_id != 6u){
  //   out_uv = uv_coords[uv_indices[gl_VertexID % 6 ]];
  // }
  out_voxel_id  = in_voxel_id;
  out_face_id = in_face_id;
  out_position_y = (m_model * vec4(in_position, 1.0)).y;
  out_uv = uv_coords[uv_indices[gl_VertexID % 6 + int(in_flip_id)*6]];
  shading = face_shading[in_face_id]* ao_ratio[in_ao_id];
}
