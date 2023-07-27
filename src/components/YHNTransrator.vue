<template>
  <div ref="container"></div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch } from 'vue'
import type { Ref } from 'vue'
import Konva from 'konva'
import ConversionTable from '../conversionTable.ts'

export default defineComponent({
  props: {
    text: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const container: Ref<HTMLDivElement | null> = ref(null)
    const stage: Ref<Konva.Stage | null> = ref(null)
    let spriteImageObj: HTMLImageElement;

    const loadImage = (src: string): Promise<HTMLImageElement> => {
      return new Promise((resolve, reject) => {
        const img = new Image()
        img.onload = () => resolve(img)
        img.onerror = reject
        img.src = src
      })
    }

    const normalizeText = (inputText: string): string => {
      // カタカナをひらがなに変換
      let normalizedText = inputText.replace(/[\u30A1-\u30F6]/g, function(match) {
        const chr = match.charCodeAt(0) - 0x60;
        return String.fromCharCode(chr);
      });

      // 大文字英数字を小文字に変換
      normalizedText = normalizedText.toLowerCase();

      return normalizedText;
    }

    const characterWidth = 50
    const lineHeight = 60

    const drawTextOnCanvas = async (spriteImageObj: HTMLImageElement) => {
      const layer = new Konva.Layer()
      stage.value!.add(layer)

      let charIndex = 0
      let currentLineY = 0;
      const canvasWidth = container.value!.clientWidth || 1000;

      const text = normalizeText(props.text)

      for (let i = 0; i < text.length; i++, charIndex++) {
        let char = text[i]

        if (i < text.length - 1 && ConversionTable[char + text[i + 1]]) {
          char += text[++i]
        }

        // Check if we need to wrap to next line
        if ((charIndex + 1) * characterWidth > canvasWidth) {
          charIndex = 0
          currentLineY += lineHeight
        }

        if (ConversionTable[char]) {
          const coords = ConversionTable[char]
          const konvaImage = new Konva.Image({
            image: spriteImageObj,
            x: charIndex * characterWidth,
            y: currentLineY,
            width: coords.w,
            height: coords.h,
            crop: {
              x: coords.x,
              y: coords.y,
              width: coords.w,
              height: coords.h,
            },
          })

          layer.add(konvaImage)
        } else {
          const text = new Konva.Text({
            text: char,
            x: charIndex * characterWidth,
            y: currentLineY,
            fontSize: 50,
            fontFamily: 'sans-serif',
            fill: 'black',
          })

          layer.add(text)
        }
      }

      layer.draw()
    }

    onMounted(async () => {
      spriteImageObj = await loadImage('/characters.png');
      
      if (!container.value) {
        return
      }

      stage.value = new Konva.Stage({
        container: container.value,
        width: container.value.clientWidth || 1000,
        height: (50 / Math.floor((container.value.clientWidth / characterWidth))) * lineHeight,
      })
      await drawTextOnCanvas(spriteImageObj);
    });

    watch(() => props.text, async () => {
      stage.value!.removeChildren()
      drawTextOnCanvas(spriteImageObj)
    });

    return { container }
  }
})
</script>
