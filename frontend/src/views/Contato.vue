<script setup>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
import { Form, Field, ErrorMessage } from 'vee-validate'
import { ref } from 'vue'
import { contatoSchema } from '@/schemas/validacoesSchema'
import { useContatoComposable } from '@/composables/useContatoComposable'

let botao = ref('block');
let preloader = ref('none');

let nome = ref('');
let email = ref('');
let telefone = ref('');
let mensagem = ref('');

const {sendData} =useContatoComposable();

let enviar =()=>{
    botao.value='none';
    preloader.value='block';
    sendData({nome:nome.value, email: email.value, telefone:telefone.value, mensagem: mensagem.value});
};

</script>

<template>
    <Header />
    <div class="breadcumb-area bg-img bg-overlay" style="background-image: url(img/bg-img/breadcumb4.jpg)">
        <div class="container h-100">
            <div class="row h-100 align-items-center">
                <div class="col-12">
                    <div class="breadcumb-text text-center">
                        <h2>Nosso Contato</h2>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <div class="contact-information-area section-padding-80">
        <div class="container">
            <div class="row">
                <div class="col-12">
                    <div class="logo mb-80">
                        <img src="/img/core-img/logo2.png" alt="" style="width: 144px;height:65px" />
                    </div>
                </div>
            </div>

            <div class="row"> 

                <div class="col-12 col-lg-12">
                    <div class="row">
                        <div class="col-4">
                            <div class="single-contact-information mb-30">
                                <h6>Endereco:</h6>
                                <p>481 Creekside Lane Avila <br />Beach, CA 93424</p>
                            </div>
                        </div>

                        <div class="col-4">
                            <div class="single-contact-information mb-30">
                                <h6>Telefones:</h6>
                                <p>+53 345 7953 32453 <br />+53 345 7557 822112</p>
                            </div>
                        </div>
                        <div class="col-4">
                            <div class="single-contact-information mb-30">
                                <h6>Email:</h6>
                                <p>{{ 'yourmail@gmail.com' }}</p>
                            </div>
                        </div>
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
                        <h3>Em que podemos ajudar!</h3>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-12">
                    <div class="contact-form-area">
                        <Form :validation-schema="contatoSchema" @submit="enviar()">

                            <div class="row">

                                <div class="col-12 col-lg-6">
                                    <ErrorMessage name="nome" class="text text-danger" />
                                    <Field type="text" name="nome" class="form-control" v-model="nome" placeholder="Nome" />
                                </div>

                                <div class="col-12 col-lg-6">
                                    <ErrorMessage name="email" class="text text-danger" />
                                    <Field type="text" name="email" class="form-control" v-model="email" placeholder="Email" />
                                </div>


                                <div class="col-12">
                                    <ErrorMessage name="telefone" class="text text-danger" />
                                    <Field type="text" name="telefone" class="form-control" v-model="telefone" placeholder="Telefone" />
                                </div>

                                <div class="col-12">
                                    <ErrorMessage name="mensagem" class="text text-danger" />
                                    <Field as="textarea" name="mensagem" class="form-control" v-model="mensagem" placeholder="Mensagem" cols="30" row="10" />
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

                        </Form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <Footer />
</template>