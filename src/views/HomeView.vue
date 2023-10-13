<template>
  <div class="home">
    <el-tabs v-model="activeName" class="tabs">
      <el-tab-pane label="XOR" name="XOR">
        <el-form :model="form1" label-width="120px" :rules="rules" ref="form1Ref">
          <el-form-item label="数据" prop="data">
            <el-input v-model="form1.data" clearable />
          </el-form-item>
          <el-form-item label="密文" v-if="form1.ciphertext">
            <el-input v-model="form1.ciphertext" disabled />
          </el-form-item>
          <el-form-item label="密钥" v-if="form1.key">
            <el-input v-model="form1.key" disabled />
          </el-form-item>
          <el-form-item label="明文" v-if="form1.plaintext">
            <el-input v-model="form1.plaintext" disabled />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit1">提交</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="Caesar" name="Caesar">
        <el-form :model="form2" label-width="120px" :rules="rules" ref="form2Ref">
          <el-form-item label="代码" prop="code">
            <el-input v-model="form2.code" clearable />
          </el-form-item>
          <el-form-item label="编码" v-if="form2.encode">
            <el-input v-model="form2.encode" disabled />
          </el-form-item>
          <el-form-item label="解码" v-if="form2.decode">
            <el-input v-model="form2.decode" disabled />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit2()">提交</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="Hill" name="Hill">
        <el-switch style="margin-bottom: 20px;" v-model="switch1" active-text="加密" inactive-text="解密" />
        <el-form v-if="switch1" :model="form3" label-width="120px" :rules="rules1" ref="form3Ref">
          <el-form-item label="明文" prop="plaintext">
            <el-input v-model="form3.plaintext" clearable />
          </el-form-item>
          <el-form-item label="矩阵" prop="matrix">
            <el-input :rows="4" type="textarea" v-model="form3.matrix" />
          </el-form-item>
          <el-form-item label="密文" v-if="form3.ciphertext">
            <el-input v-model="form3.ciphertext" disabled />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit3('encode')">加密</el-button>
          </el-form-item>
        </el-form>
        <el-form v-if="!switch1" :model="form3" label-width="120px" :rules="rules2" ref="form3Ref">
          <el-form-item label="密文" prop="ciphertext">
            <el-input v-model="form3.ciphertext" clearable />
          </el-form-item>
          <el-form-item label="矩阵" prop="matrix">
            <el-input :rows="4" type="textarea" v-model="form3.matrix" />
          </el-form-item>
          <el-form-item label="明文" v-if="form3.plaintext">
            <el-input v-model="form3.plaintext" disabled />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit3('decode')">解密</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="DH" name="DH">
        <el-form :model="form4" label-width="120px" :rules="rules" ref="form4Ref">
          <el-form-item label="数字" prop="number">
            <el-input v-model="form4.number" clearable />
          </el-form-item>
          <el-form-item label="密钥" v-if="form4.key">
            <el-input v-model="form4.key" disabled />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit4">提交</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="RSA" name="RSA">
        <el-form :model="form5" label-width="120px" :rules="rules" ref="form5Ref">
          <el-form-item label="MSG" prop="msg">
            <el-input v-model="form5.msg" clearable />
          </el-form-item>
          <el-form-item label="P" prop="p">
            <el-input v-model="form5.p" clearable />
          </el-form-item>
          <el-form-item label="Q" prop="q">
            <el-input v-model="form5.q" clearable />
          </el-form-item>
          <el-form-item label="E" prop="e">
            <el-input v-model="form5.e" clearable />
          </el-form-item>
          <el-form-item label="N" v-if="form5.n">
            <el-input v-model="form5.n" disabled />
          </el-form-item>
          <el-form-item label="C" v-if="form5.c">
            <el-input v-model="form5.c" disabled />
          </el-form-item>
          <el-form-item label="D" v-if="form5.d">
            <el-input v-model="form5.d" disabled />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit5">提交</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="Hash" name="Hash">
        <el-form :model="form6" label-width="120px" :rules="rules" ref="form6Ref">
          <el-form-item label="文件1" prop="txt1">
            <el-input v-model="form6.txt1" clearable />
          </el-form-item>
          <el-form-item label="文件2" prop="txt2">
            <el-input v-model="form6.txt2" clearable />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit6">提交</el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>

  </div>
</template>


<script lang="ts" setup>
import { reactive, ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus';

const activeName = ref('XOR')
const switch1 = ref(true)

const form1 = reactive({
  data: '',
  ciphertext: '',
  key: '',
  plaintext: ''
})

const form2 = reactive({
  code: '',
  encode: '',
  decode: ''
})

const form3 = reactive({
  mode: '',
  ciphertext: '',
  matrix: '',
  plaintext: ''
})

const form4 = reactive({
  number: '',
  key: ''
})

const form5 = reactive({
  msg: '',
  p: '',
  q: '',
  e: '',
  n: '',
  c: '',
  d: ''
})

const form6 = reactive({
  txt1: '',
  txt2: ''
})

const rules = {
  data: [
    { required: true, message: '请输入数据', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入代码', trigger: 'blur' }
  ],
  plaintext: [
    { required: true, message: '请输入明文', trigger: 'blur' }
  ],
  number: [
    { required: true, message: '请输入数字', trigger: 'blur' }
  ],
  msg: [
    { required: true, message: '请输入MSG', trigger: 'blur' }
  ],
  p: [
    { required: true, message: '请输入P', trigger: 'blur' }
  ],
  q: [
    { required: true, message: '请输入Q', trigger: 'blur' }
  ],
  e: [
    { required: true, message: '请输入E', trigger: 'blur' }
  ],
  txt1: [
    { required: true, message: '请输入文件1', trigger: 'blur' }
  ],
  txt2: [
    { required: true, message: '请输入文件2', trigger: 'blur' }
  ]
}

const rules1 = {
  plaintext: [
    { required: true, message: '请输入明文', trigger: 'blur' }
  ],
  matrix: [
    { required: true, message: '请输入矩阵', trigger: 'blur' }
  ]
}

const rules2 = {
  ciphertext: [
    { required: true, message: '请输入密文', trigger: 'blur' }
  ],
  matrix: [
    { required: true, message: '请输入矩阵', trigger: 'blur' }
  ]
}

const form1Ref = ref()
const form2Ref = ref()
const form3Ref = ref()
const form4Ref = ref()
const form5Ref = ref()
const form6Ref = ref()

const onSubmit1 = async () => {
  form1Ref.value.validate((valid: any) => {
    if (valid) {
      axios.post('http://127.0.0.1:25565/api/XOR', form1)
        .then(response => {
          form1.ciphertext = response.data.encrypted
          form1.plaintext = response.data.decrypted
          form1.key = response.data.key
        })
        .catch(error => {
          console.error(error)
        })
    }
  })
}

const onSubmit2 = async () => {
  form2Ref.value.validate((valid: any) => {
    if (valid) {
      axios.post('http://127.0.0.1:25565/api/Caesar', form2)
        .then(response => {
          form2.encode = response.data.encode
          form2.decode = response.data.decode
        })
        .catch(error => {
          console.error(error)
        })
    }
  })
}

const onSubmit3 = async (mode: any) => {
  form3Ref.value.validate((valid: any) => {
    if (valid) {
      if (mode == 'encode') {
        form3.mode = mode
        axios.post('http://127.0.0.1:25565/api/Hill', form3)
          .then(response => {
            if (response.data.error) {
              ElMessage({
                message: response.data.error,
                type: 'error',
              })
            }
            form3.ciphertext = response.data.result
          })
          .catch(error => {
            console.error(error)
          })
      } else {
        form3.mode = mode
        axios.post('http://127.0.0.1:25565/api/Hill', form3)
          .then(response => {
            if (response.data.error) {
              ElMessage({
                message: response.data.error,
                type: 'error',
              })
            } else {
              form3.plaintext = response.data.result
            }
          })
          .catch(error => {
            console.error(error)
          })
      }
    }
  })
}

const onSubmit4 = async () => {
  form4Ref.value.validate((valid: any) => {
    if (valid) {
      axios.post('http://127.0.0.1:25565/api/DH', form4)
        .then(response => {
          if (response.data.error) {
            ElMessage({
              message: response.data.error,
              type: 'error',
            })
          } else {
            form4.key = response.data.key
          }
        })
        .catch(error => {
          console.error(error)
        })
    }
  })
}

const onSubmit5 = async () => {
  form5Ref.value.validate((valid: any) => {
    if (valid) {
      axios.post('http://127.0.0.1:25565/api/RSA', form5)
        .then(response => {
          form5.n = response.data.n
          form5.c = response.data.c
          form5.d = response.data.d
        })
        .catch(error => {
          console.error(error)
        })
    }
  })
}

const onSubmit6 = async () => {
  form6Ref.value.validate((valid: any) => {
    if (valid) {
      axios.post('http://127.0.0.1:25565/api/HASH', form6)
        .then(response => {
          ElMessage({
            message: response.data.message,
            type: 'success',
          })
        })
        .catch(error => {
          console.error(error)
        })
    }
  })
}

</script>

<style>
.home {
  position: relative;
  left: 20%;
  top: 150px;
  width: 60%;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border: 5px solid #ebeef5;
  /* background-color: rgb(240, 242, 245); */
  background-color: #f0f2f5;
  padding: 20px;
}

.tabs>.el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
</style>
