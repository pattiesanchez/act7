<script setup>
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import { receitaComposable } from '@/composables/receitaCompos';
import {useRoute} from 'vue-router';
import { watchEffect } from 'vue';

let route = useRoute();

const {dado:dado, error: error} = receitaComposable(route.params.slug);
 
watchEffect(()=>
{
    if(error.value)
    {
        window.location="/error";
    }
});
</script>

<template>
    <Header />
    <div class="breadcumb-area bg-img bg-overlay" style="background-image: url(/img/bg-img/breadcumb4.jpg)">
        <div class="container h-100">
          <div class="row h-100 align-items-center">
            <div class="col-12">
              <div class="breadcumb-text text-center">
                <h2>{{ dado.data?.nome }}</h2>
              </div>
            </div>
          </div>
        </div>
        </div>

        <div class="receipe-post-area section-padding-80">


  <div class="container">
      <div class="row">
          <div class="col-12">
            <img :src="dado.data?.imagem" :alt="dado.data?.nome" />
          </div>
      </div>
  </div>

  <div class="receipe-content-area">
      <div class="container">

          <div class="row">
              <div class="col-12 col-md-8">
                  <div class="receipe-headline my-5">
                      <span>{{ dado.data?.data }}</span>
                      <h2>{{ dado.data?.nome }}</h2>
                      <div class="receipe-duration">
                          <h6>Tempo : {{ dado.data?.tempo }}</h6>
                          <h6>Categoria: {{ dado.data?.categoria }}</h6>
                          <h6>Criada por: {{ dado.data?.user }}</h6>
                      </div>
                  </div>
              </div>


          </div>

          <div class="row">
              <div class="col-12 col-lg-12">
                  <div class="single-preparation-step d-flex">

                      <p> {{ dado.data?.descricao }} </p>
                  </div>

              </div>

          </div>


      </div>
  </div>
</div>
    <Footer />
  </template>
 