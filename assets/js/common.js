$(document).ready(function(){$("a.abstract").click(function(){$(this).parent().parent().find(".abstract.hidden").toggleClass("open")}),$("a.bibtex").click(function(){$(this).parent().parent().find(".bibtex.hidden").toggleClass("open")}),$("a").removeClass("waves-effect waves-light")}),document.addEventListener("DOMContentLoaded",function(){new ClipboardJS(".copy-bibtex",{text:function(e){const t=e.getAttribute("data-clipboard-target");return document.querySelector(t).textContent.trim()}}),document.querySelectorAll(".copy-bibtex").forEach(e=>{e.addEventListener("click",()=>{e.innerHTML='<i class="fas fa-check"></i> Copied!',setTimeout(()=>{e.innerHTML='<i class="fas fa-copy"></i> Copy'},2e3),window.getSelection?window.getSelection().removeAllRanges():document.selection&&document.selection.empty()})})});