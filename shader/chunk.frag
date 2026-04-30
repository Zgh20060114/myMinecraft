#version 330 core
layout(location=0) out vec4 frag_color;
in vec2 out_uv;
in vec3 out_voxel_color;
uniform sampler2D texture_0;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

void main(){
  // gl_FragColor = vec4(0, 0, 0, 1)
  vec3 texture_color = texture(texture_0,out_uv).rgb;
  texture_color = pow(texture_color,gamma ); // 线性空间
  texture_color *= out_voxel_color;
  texture_color = pow(texture_color, inv_gamma);
  frag_color = vec4(texture_color,1.0f);
}
