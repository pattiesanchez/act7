<script setup>
import Footer from '@/components/Footer.vue';
import Header from '@/components/Header.vue';
import { onMounted, onUnmounted, ref } from 'vue';
import {Form, Field, ErrorMessage} from 'vee-validate';

import {receitasSchema} from '@/schemas/validacoesSchema';
import axios from 'axios';

import { Fancybox } from '@fancyapps/ui/dist/fancybox/'
import '@fancyapps/ui/dist/fancybox/fancybox.css'

let dados = ref([]);
let categorias = ref([]);

onMounted(async ()=>{
    let resposta =  await fetch(`${import.meta.env.VITE_API_URL}receitas-painel/${localStorage.getItem('receitas_flaites_id')}`, {
        headers:{'content-type':'application/json', 'Authorization': `Bearer ${localStorage.getItem('receitas_flaites_token')}`}
    });
    dados.value = await resposta.json();

    let resposta2 =  await fetch(`${import.meta.env.VITE_API_URL}categorias`, {
        headers:{'content-type':'application/json'}
    });
    categorias.value = await resposta2.json();

    Fancybox.bind('[data-fancybox]', {})
   
});

onUnmounted(() => {
  Fancybox.unbind('[data-fancybox]')
  Fancybox.close()
})

let nome = ref('');
let tempo = ref('');
let descricao = ref('');
let categoria_id = ref('0');
let receitas_id=ref('0');
let botao  = ref('block');
let preloader  = ref('none');

let enviar=()=>
{ 
    botao.value="none";
    preloader.value="block";
    if(modal_titulo.value=="Criar")
    {
        let file = document.querySelector("input[type=file]").files[0];
        let formData =new FormData();
        formData.append('foto', file);
        formData.append('categoria_id', categoria_id.value);
        formData.append('nome', nome.value);
        formData.append('tempo', tempo.value);
        formData.append('descricao', descricao.value);
       
        axios.post(`${import.meta.env.VITE_API_URL}receitas`, formData, 
            {headers:{'Authorization': `Bearer ${localStorage.getItem('receitas_flaites_token')}`}})
        .then((response)=>{
            alert("Registro criado com sucesso");
            window.location="/painel";
        })
        .catch((err)=>{
            alert("Ocorreu um erro inesperado "+err);
            window.location="/painel";
        });
    }
    if(modal_titulo.value=="Editar")
    {
        axios.put(`${import.meta.env.VITE_API_URL}receitas/${receitas_id.value}`, 
            {nome:nome.value, tempo: tempo.value, descricao:descricao.value, categoria_id: categoria_id.value}, 
            {headers:{'Authorization': `Bearer ${localStorage.getItem('receitas_flaites_token')}`}})
        .then((response)=>{
            alert("Registro modificado com sucesso");
            window.location="/painel";
        })
        .catch((err)=>{
            alert("Ocorreu um erro inesperado "+err);
            window.location="/painel";
        });
    }
};


let modal_titulo = ref('');
let criar =()=>
{
    modal_titulo.value='Criar';
    categoria_id.value='0';
    nome.value='';
    tempo.value='';
    descricao.value='';
};
let editar =(modelo)=>
{
    modal_titulo.value='Editar';
    receitas_id.value=modelo.id;
    categoria_id.value=modelo.categoria_id;
    nome.value=modelo.nome;
    tempo.value=modelo.tempo;
    descricao.value=modelo.descricao;
};
const deletar=(id)=>
{
    if(window.confirm("Realmente deseja deletar o registro?"))
    {
        axios.delete(`${import.meta.env.VITE_API_URL}receitas/${id}`, {headers:{'Authorization': `Bearer ${localStorage.getItem('receitas_flaites_token')}`}})
        .then((response)=>{
            alert("Registro deletado com sucesso");
            window.location="/painel";
        })
        .catch((err)=>{
            alert("Ocorreu um erro inesperado "+err);
            window.location="/painel";
        });
    }
};
</script>

<template>
    <Header />
    <div class="breadcumb-area bg-img bg-overlay" style="background-image: url(img/bg-img/breadcumb6.jpg)">
        <div class="container h-100">
          <div class="row h-100 align-items-center">
            <div class="col-12">
              <div class="breadcumb-text text-center">
                <h2>Painel</h2>
              </div>
            </div>
          </div>
        </div>
      </div>


      <div class="contact-area section-padding-0-80">
        <div class="container">
          <div class="row">
            <div class="col-12">
              <div class="section-heading">
                <h3>Minhas receitas publicadas</h3>
              </div>
            </div>
          </div>

          <div class="row">
            <div class="col-12">
              <div class="receipe-ratings text-right my-5">
                <a href="#modal2" @click="criar()" class="btn delicious-btn"><i class="fas fa-plus"></i>Criar</a>
              </div>
            </div>
            <hr />
            <div class="col-12">
              <div class="table-responsive">
                <table class="table table-bordered table-hover table-striped">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Categoria</th>
                      <th>Nome</th>
                      <th>Tempo</th>
                      <th>Detalhes</th>
                      <th>Foto</th>
                      <th>Acoes</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(dado, index) in dados.data" :key="index">
                        <td>{{ dado.id }}</td>
                        <td>{{ dado['categoria'] }}</td>
                        <td>{{ dado.nome }}</td>
                        <td>{{ dado.tempo }}</td>
                        <td>{{ dado.descricao }}</td>
                        <td class="text-center">
                            <a :href="dado.imagem" class="lightbox d-block" data-fancybox="image-gallery">
                                <img :src="dado.imagem" :alt="dado.nome" style="width: 100px;" />
                            </a>
                        </td>
                        <td class="text-center">
                            <router-link :to="{name:'painel_editar', params:{id:dado.id}}" title="Editar foto">
                                <i class="fas fa-pen-square"></i>
                            </router-link>    
                            &nbsp;&nbsp;
                            <a href="#modal2" title="Editar" @click="editar(dado)">
                                <i class="fas fa-edit"></i>
                            </a>
                            &nbsp;&nbsp;
                            <router-link to="#" @click.navigate="deletar(dado.id)" title="Deletar">
                                <i class="fas fa-trash"></i>
                            </router-link>
                        </td>
                    </tr>
                  </tbody>
                 
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    <Footer />
    <!--modal-->
      <div class="modalmask" id="modal2">
        <div class="modalbox rotate">
            <a href="#close" title="Fechar" class="close">X</a>
            <h2>{{modal_titulo}}</h2>
                <Form :validation-schema="receitasSchema" @submit="enviar()">
                    <div class="contact-form-area">
                    <div class="row container">

                        <div class="col-12 col-lg-12">
                            <ErrorMessage name="categoria_id" class="text text-danger" />
                            <Field as="select" name="categoria_id" v-model="categoria_id" class="form-control" style="height: calc(2.25rem + 10px);">
                                <option value="0">Selecione.....</option>
                                <option v-for="(categoria, i) in categorias.data" :key="i" :value="categoria.id">{{categoria.nome}}</option>
                            </Field>
                        </div>

                        <div class="col-12 col-lg-12">
                            <ErrorMessage name="nome" class="text text-danger" />
                            <Field type="text" name="nome" v-model="nome" placeholder="nome" class="form-control" />
                        </div>

                        <div class="col-12 col-lg-12">
                            <ErrorMessage name="tempo" class="text text-danger" />
                            <Field type="text" name="tempo" v-model="tempo" placeholder="tempo" class="form-control" />
                        </div>

                        <div class="col-12 col-lg-12">
                            <ErrorMessage name="descricao" class="text text-danger" />
                            <Field as="textarea" name="descricao" v-model="descricao" placeholder="Descripción" class="form-control" />
                        </div>

                        <div v-if="modal_titulo=='Criar'" class="col-12 col-lg-12">
                            <input type="file" name="foto" id="file" class="form-control" />
                        </div>

                        <div class="col-12 text-center" :style="'display:'+botao">
                            <button class="btn delicious-btn mt-30" type="submit" title="Enviar">
                                Enviar
                            </button>
                        </div>
                        <div class="col-12 text-center" :style="'display:'+preloader">
                            <img src="/img/img/load.gif" />
                        </div>

                    </div>
                </div>
                </Form>
        </div>
      </div>
    <!--/modal-->
</template>
<style scoped>
.modalmask {
  position: fixed;
  font-family: Arial, sans-serif;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  background: rgba(0, 0, 0, 0.8);
  z-index: 99999;
  opacity: 0;
  -webkit-transition: opacity 400ms ease-in;
  -moz-transition: opacity 400ms ease-in;
  transition: opacity 400ms ease-in;
  pointer-events: none;
}

.modalmask:target {
  opacity: 1;
  pointer-events: auto;
}

.modalbox {
  width: 600px;
  position: relative;
  padding: 5px 20px 13px 20px;
  background: #fff;
  border-radius: 3px;
  -webkit-transition: all 500ms ease-in;
  -moz-transition: all 500ms ease-in;
  transition: all 500ms ease-in;

}

.rotate {
  margin: 1% auto;
  -webkit-transform: scale(-5, -5);
  transform: scale(-5, -5);
}


.modalmask:target .rotate {
  transform: rotate(360deg) scale(1, 1);
  -webkit-transform: rotate(360deg) scale(1, 1);
}

.close {
  background: #606061;
  color: #FFFFFF;
  line-height: 25px;
  position: absolute;
  right: 1px;
  text-align: center;
  top: 1px;
  width: 24px;
  text-decoration: none;
  font-weight: bold;
  border-radius: 3px;

}

.close:hover {
  background: #FAAC58;
  color: #222;
}
</style>