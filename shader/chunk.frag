#version 330 core
layout(location=0) out vec4 frag_color;
in vec3 out_color;

void main(){
  // gl_FragColor = vec4(0, 0, 0, 1)
  frag_color = vec4(out_color,1.0f);
}
