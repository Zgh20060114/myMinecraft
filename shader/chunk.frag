#version 330 core
layout(location=0) out vec4 frag_color;
in vec2 out_uv;
// in vec3 out_voxel_color;
in float shading;
uniform sampler2DArray texture_array; // 底面0,侧面1345,顶面2
flat in uint out_voxel_id;
flat in uint out_face_id;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

void main(){
  uint face_id;
  vec2 uv;
  // gl_FragColor = vec4(0, 0, 0, 1)
  if(out_face_id == 1u ||out_face_id == 3u||out_face_id == 4u ||out_face_id == 5u){
    face_id = 1u;
  }else{
    face_id = out_face_id;
  }
  uv.x = (out_uv.x+ face_id) / 3.0;
  uv.y = out_uv.y;
  vec3 texture_color = texture(texture_array,vec3(uv,out_voxel_id)).rgb;
  texture_color = pow(texture_color,gamma ); // 线性空间
  // texture_color *= out_voxel_color;
  texture_color = pow(texture_color*shading, inv_gamma);
  frag_color = vec4(texture_color,1.0f);
}
